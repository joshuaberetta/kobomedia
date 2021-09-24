#!/usr/bin/env python3

import argparse
import json
import os
import re
import requests


def download_all_media(data_url, stats, *args, **kwargs):

    data_res = requests.get(
        data_url, headers=kwargs['headers'], params=kwargs['params']
    )
    if data_res.status_code != 200:
        return stats

    data = data_res.json()
    next_url = data['next']
    results = data['results']

    if not results:
        return stats

    for sub in results:
        if not '_attachments' in sub:
            continue

        if not sub['_attachments']:
            continue

        sub_dir = os.path.join(kwargs['asset_uid'], sub['_uuid'])
        if not os.path.isdir(sub_dir):
            os.makedirs(sub_dir)

        for attachment in sub['_attachments']:
            download_url = attachment['download_url']
            filename = get_filename(attachment['filename'])
            file_path = os.path.join(sub_dir, filename)
            if os.path.exists(file_path):
                if kwargs['verbosity'] == 3:
                    print(f'File already exists, skipping: {file_path}')
                stats['skipped'] += 1
                continue
            download_media_file(
                url=download_url, path=file_path, stats=stats, *args, **kwargs
            )

    if next_url is not None:
        download_all_media(data_url=next_url, stats=stats, *args, **kwargs)

    return stats


def download_media_file(url, path, stats, headers, chunk_size, *args, **kwargs):
    stream_res = requests.get(url, stream=True, headers=headers)
    if stream_res.status_code != 200:
        if kwargs['verbosity'] == 3:
            print(f'Fail: {path}')
        stats['failed'] += 1
        return stats

    with open(path, 'wb') as f:
        for chunk in stream_res.iter_content(chunk_size):
            f.write(chunk)

    if kwargs['verbosity'] == 3:
        print(f'Success: {path}')
    stats['successful'] += 1

    return stats


def get_clean_stats():
    return {'successful': 0, 'failed': 0, 'skipped': 0}


def get_data_url(asset_uid, kf_url):
    return f'{kf_url}/api/v2/assets/{asset_uid}/data'


def get_filename(path):
    return path.split('/')[-1]


def get_kf_url_and_asset_uid(url):
    return re.match(
        r'^(https?://[a-z\.]*).*(a[a-zA-Z0-9]{21}).*$', url
    ).groups()


def get_params(limit=100, query='', *args, **kwargs):
    params = {'format': 'json', 'limit': limit}
    if query:
        params['query'] = query
    return params


def main(url, token, verbosity=3, *args, **kwargs):
    kf_url, asset_uid = get_kf_url_and_asset_uid(url)
    options = {
        'asset_uid': asset_uid,
        'params': get_params(*args, **kwargs),
        'headers': {'Authorization': f'Token {token}'},
        'verbosity': verbosity,
    }
    data_url = get_data_url(asset_uid, kf_url)
    stats = download_all_media(
        data_url, stats=get_clean_stats(), *args, **kwargs, **options
    )
    if verbosity > 1:
        print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A CLI tool to download kobo media files'
    )
    parser.add_argument(
        '--url',
        '-u',
        type=str,
        help='Kobo URL',
        required=True,
    )
    parser.add_argument(
        '--token',
        '-t',
        type=str,
        help='Authentication token',
        required=True,
    )
    parser.add_argument(
        '--limit',
        '-l',
        type=int,
        default=100,
        help='Query limit',
    )
    parser.add_argument(
        '--query',
        '-q',
        type=str,
        default='',
        help='Custom data query',
    )
    parser.add_argument(
        '--chunk-size',
        '-c',
        type=int,
        default=1024,
        help='Stream chunk size',
    )
    parser.add_argument(
        '--verbosity',
        '-v',
        type=int,
        default=3,
        help='Output verbosity',
    )
    args = parser.parse_args()

    main(
        url=args.url,
        token=args.token,
        limit=args.limit,
        query=args.query,
        chunk_size=args.chunk_size,
        verbosity=args.verbosity,
    )
