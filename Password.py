import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code},check the API')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    hash_p_wd = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5_char, tail = hash_p_wd[:5], hash_p_wd[5:]
    response = request_api_data(first_5_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for item in args:
        count = pwned_api_check(item)
        if count:
            print(f'{item} was found {count} times..., You should probably change your password!')
        else:
            print(f'{item} was NOT found. Carry on!')
    return "done!"


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
