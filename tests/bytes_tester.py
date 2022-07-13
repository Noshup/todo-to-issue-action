import os
import requests
import json
import base64
import re


class TestGitHubClient(object):
    contents_url = 'https://api.github.com/repos/Noshup/noshup-marketplace/contents'
    token = None
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'token {token}'
    }

    def _get_code_source(self, file_path, start, end):
        file_url = f'{self.contents_url}/{file_path}'
        file = None
        file_json = None
        file_content = None
        file_content_64 = None
        lines_64 = None

        lines_str = []
        target_lines = []
        target_string = ""

        file_blob_request = requests.get(file_url, headers=self.headers)

        if file_blob_request.status_code == 200:
            print("Request Succeeded!")
            file = file_blob_request.text
            file_json = json.loads(file)
            file_content = file_json["content"]
            file_content_64 = bytes(file_content, 'raw_unicode_escape')
            lines_64 = file_content.split('\n')
            print("Content Type = ", type(file_content))
            print("Contents = \n", file_content)
            print("\nContents By Line: \n", lines_64,
                  "\nNumber of Lines = ", len(lines_64))

            print("\nContent base64 = ", file_content_64)
            str_content = base64.b64decode(file_content_64)

            print("\nDecoded Content = ", str_content)

            lines_str = str_content.split(b'\n')
            print("\nSplit String Content: \n", lines_str)

            print("\nTarget Line Numbers = ", start, " -> ", end)
            start_a = start-1
            end_a = end+1
            for x in range(start_a, end_a):
                target_lines.append(lines_str[x])
            print("\nTarget Lines: ", target_lines)

            for x in target_lines:
                str_actual = x.decode('utf-8')
                target_string = target_string+str_actual+'\n'

            print("\n Target String: \n\n", target_string)

        else:
            print("Success Did not Succeed! Status = ",
                  file_blob_request.status_code)


def _get_hunk_lines(comment):
    CODE_LINES_PATTERN = re.compile(r'(?<=lines:\s).+')
    lines_search = CODE_LINES_PATTERN.search(comment, re.IGNORECASE)
    value = None
    lines = None
    if lines_search:
        value = lines_search.group(0)
        print("get_hunk_lines: Raw Value =", value)
        value_p = value.strip(' ')
        lines = value_p.split(',')
        start = int(lines[0])
        end = int(lines[1])
        lines = [start, end]
        print("get_hunk_lines: Lines =", lines)
    else:
        print("get_hunk_lines: Could not find Hunk Lines in Comment Line!")

    return lines


def main():
    test_line_nums = 'lines: 15,28'
    lines = _get_hunk_lines(test_line_nums)

    client = TestGitHubClient()
    client._get_code_source(
        'lib/constants/delivery_constants.dart', lines[0], lines[1])


main()
