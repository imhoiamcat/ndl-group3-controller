import csv
import os
from typing import List, Dict, Union

from paramiko import SSHClient, AutoAddPolicy, RSAKey
from scp import SCPClient


class FileTransfer:
    def __init__(self, file_path=None, save_path=None):
        self.__rsa_key = self.__load_rsa_key()
        self.__connection_credentials = self.__load_credentials()
        self.__default_save_path = self.__load_default_save_path()

        self.__ssh = SSHClient()
        self.__connection_established = False

        self.__host = self.__connection_credentials["host"].strip()
        self.__username = self.__connection_credentials["username"].strip()

        if save_path is not None:
            self.__save_path = save_path.strip()
        else:
            self.__save_path = self.__default_save_path["path"].strip()

        self.__temp_dir = self.__save_path + "/tmp/"

        if file_path is not None:
            self.__file_path = file_path.strip()
        else:
            self.__file_path = ""

    @classmethod
    def __load_rsa_key(cls) -> RSAKey:
        try:
            with open("resources/ssh_info/key.pem") as key_file:
                return RSAKey.from_private_key(key_file)
        except Exception as e:
            raise ValueError(f"Failed to load RSA key: {e}")

    @classmethod
    def __load_credentials(cls) -> str:
        try:
            with open("resources/ssh_info/credentials.csv") as credentials_file:
                reader = csv.DictReader(credentials_file, fieldnames=["host", "username"])
                return next(reader)
        except Exception as e:
            raise ValueError(f"Failed to load SSH credentials: {e}")

    @classmethod
    def __load_default_save_path(cls) -> str:
        try:
            with open("resources/ssh_info/default_save_path.csv") as default_save:
                reader = csv.DictReader(default_save, fieldnames=["path"])
                return next(reader)
        except Exception as e:
            raise ValueError(f"Failed to load Default Save Path: {e}")

    def __connect(self) -> None:
        try:
            self.__ssh.set_missing_host_key_policy(AutoAddPolicy())
            self.__ssh.connect(hostname=self.__host, username=self.__username, pkey=self.__rsa_key)
            self.__connection_established = True
        except Exception as e:
            raise ConnectionError(f"Could not connect to the server: {e}")

    def __find_existing_files(self) -> Union[bool, List]:
        if not self.__connection_established:
            try:
                self.__connect()
            except ConnectionError:
                return False

        try:
            sftp = self.__ssh.open_sftp()

            if os.path.isdir(self.__file_path):
                existing_files = []
                for y in os.listdir(self.__file_path):
                    file = os.path.join(self.__save_path, y)
                    linux_path = file.replace('\\', '/')
                    try:
                        sftp.stat(linux_path)
                        existing_files.append(y)
                    except IOError:
                        # if sftp.stat() throws an exception the file does not exist, so we continue checking
                        continue

                if len(existing_files) is 0:
                    return False, None
                else:
                    return True, existing_files
            else:
                try:
                    file_name = os.path.basename(self.__file_path)
                    file = os.path.join(self.__save_path, file_name)
                    linux_path = file.replace('\\', '/')
                    sftp.stat(linux_path)
                    return True, [file_name]
                except IOError:
                    # if sftp.stat() throws an exception the file does not exist
                    return False, None

        except ConnectionError:
            raise ConnectionError("Could not connect to the server to check if file exists")

    def file_transfer(self) -> Union[bool, Dict]:
        if not self.__connection_established:
            try:
                self.__connect()
            except ConnectionError:
                return False
                
        existing_files = []
        try:
            exists, existing_files = self.__find_existing_files()
            if exists:
                raise IOError("Some of the files already exist on the server")
        except ConnectionError:
            return False
        except IOError:
            return False, {"existing_files": existing_files}

        try:
            self.__ssh.exec_command(f"mkdir {self.__temp_dir}")
            scp = SCPClient(self.__ssh.get_transport())
            if os.path.isdir(self.__file_path):
                for x in os.listdir(self.__file_path):
                    # transfer image to the server via SSH
                    file = os.path.join(self.__file_path, x)
                    scp.put(file, recursive=False, remote_path=self.__temp_dir)
            else:
                # transfer image to the server via SSH
                scp.put(self.__file_path, recursive=False, remote_path=self.__temp_dir)

            scp.close()
            # if transfer was fine and not aborted unpack the files to the main __save_path
            self.__unpack_temp_dir()
            self.__remove_temp_dir()
            return True
        except Exception:
            self.__remove_temp_dir()
            return False

    def __remove_temp_dir(self) -> None:
        self.__ssh.exec_command(f"rm -rf {self.__temp_dir}")

    def __unpack_temp_dir(self) -> None:
        self.__ssh.exec_command(f"mv {self.__temp_dir}/* {self.__save_path}")

    def delete_file(self, resource: str, id_to_be_deleted: int) -> bool:
        if not self.__connection_established:
            try:
                self.__connect()
            except ConnectionError:
                return False

        try:
            file_name = os.path.basename(resource)
            file = os.path.join(self.__save_path, file_name)
            linux_path = file.replace('\\', '/')
            self.__ssh.exec_command(f"rm {linux_path}")

            return True
        except Exception as e:
            raise e

    def abort(self) -> bool:
        if self.__connection_established:
            try:
                self.__remove_temp_dir()
                self.__ssh.close()
                self.__connection_established = False
                return True
            except ConnectionResetError:
                return False

    def close_connection(self) -> bool:
        try:
            self.__ssh.close()
            self.__connection_established = False
            return True
        except ConnectionResetError:
            return False
