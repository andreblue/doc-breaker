# Doc Breaker

This is a simple tool to allow you to brute force docx and such files thru python.

It uses [msoffcrypto-tool](https://github.com/nolze/msoffcrypto-tool) and uses [danielmiessler/SecLists
](https://github.com/danielmiessler/SecLists) password list for the common 10000 passwords.

The 10000 password list will download if it can not find it. Thus no setup is needed for that.

## Disclaimer
This is made for educational purposes or for documents that you created and have forgotten the password. I take no responsablity for any misdeeds this is used for.

## Requirements

##### Python 3

##### Install the msoffcrypto-tool with:

```pip install msoffcrypto-tool```


## Usage

```python doc-break.py <options>```

| Option        | Long Option| Requirements  |
| :-------------: |:-------------:| :-----:|
| -i      | --ifile | File path to file |
| -c      | --common | Uses the 10000 common password list |
| -v      | --verbose | Outputs current password and progress thru the list |
| -l      | --list | File path to the list file |
