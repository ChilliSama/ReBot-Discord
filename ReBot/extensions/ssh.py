# from base64 import decode
# import paramiko
from os import replace
from pexpect import pxssh
import getpass
from rich import print
import lightbulb
import re

plugin = lightbulb.Plugin("Admin")


class pyssh():

    def __init__(self, ip, port, username, password) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        self.s = pxssh.pxssh()

    def get_prompt(self):
        try:
            self.s.sendline('pwd')
            self.s.prompt()
            line = self.s.before.decode().replace('\r\n', '').replace('\r', '').replace('pwd', '').replace('/home', '').replace('/bts', '')
            line = self.ansi_escape.sub('', line)
            print('\n')
            print(self.s.before)
            print(repr(line))
            line = str(self.username) + "~" + line + "$> " 
            print(line)
            return line
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on prompt.")
            print(e)

    def connect(self):
        try:
            self.s.login(self.ip, self.username, self.password, port=self.port)
            self.out = self.get_prompt()
            return "```diff\r" + self.out + " ```"
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)

    def send_cmd(self, cmd):
        try:
            self.s.sendline(cmd)
            self.s.prompt()
            line = self.s.before.decode().replace('\r\n', '').replace('\r', '').replace(cmd, '')
            line = self.ansi_escape.sub('', line)
            print('\n')
            print(self.s.before)
            print(repr(line)) 
            prompt = self.get_prompt()
            self.out = self.out + '\r' + prompt + cmd + '\r' + line
            print(self.out)
            return "```diff\r" + self.out + " ```"
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on send cmd.")
            print(e)
    
    def logout(self):
        try:
            self.s.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on logout.")
            print(e)



# class pyssh():
#     session = SSHClient()

    # def __init__(self, ip, port, username, password) -> None:
    #     self.ip = ip
    #     self.port = port
    #     self.username = username
    #     self.password = password

#     def check_error(self):
#         if self.stdself.out.channel.recv_exit_status() != 0:
#             return  (type(self.stdself.out.channel.recv_exit_status()) + self.stdself.out.channel.recv_exit_status())
#             # raise Exception('There was an error pulling the runtime: {}'.format(self.stderr))
#         else:
#             return self.stdself.out

#     def set_command(self, cmd_in):
#         self.stdin, self.stdself.out, self.stderr = self.session.exec_command(cmd_in)

#     def print_prompt(self):
#         self.stdin, self.stdself.out, self.stderr = self.session.exec_command("pwd")
#         self.stdself.out = self.stdself.out.read().decode().strip()
#         self.stderr = self.stderr.read().decode().strip()
#         self.stdself.out = self.stdself.out + "$>"

#     def close_session(self):
#         self.stdin.close()
#         self.stdself.out.close()
#         self.stderr.close()
#         self.session.close()

#     def connection(self):
#         if not self.is_connected():
#             self.session.load_system_host_keys()
#             self.session.set_missing_host_key_policy(AutoAddPolicy())
#             self.session.connect(self.ip, port= self.port, username= self.username, password= self.password, look_for_keys=False, allow_agent=False)

#     def is_connected(self):
#         transport = self.session.get_transport() if self.session else None
#         return transport and transport.is_active()

#     def connect(self):
#         self.connection()
#         self.set_command("pwd")
#         return self.check_error()



def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)



# client = SSHClient()
# client.load_host_keys()
# client.load_system_host_keys()
# client.set_missing_host_key_policy(AutoAddPolicy())
# client.connect('', username='', password="")

# stdin, stdself.out, stderr = client.exec_command('hostname')
# print(type(stdin))
# print(type(stdself.out))
# print(type(stderr))

# stdin.write('Hello world')
# stdin.channel.shutdown_write()

# print(f'STDself.out: {stdself.out.read().decode("utf8")}')
# print(f'STDERR: {stderr.read().decode("utf8")}')

# print(f'Return code: {stdself.out.channel.recv_exit_status()}')

# stdin.close()
# stdself.out.close()
# stderr.close()

# client.close()