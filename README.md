## Setup

```bash
git clone https://github.com/joshuaberetta/kobomedia
cd kobomedia

# optional
chmod +x kobomedia.py
sudo ln -s $(pwd)/kobomedia.py /usr/local/bin/kobomedia
```

Create `kobo.json` config file with the following settings:

```json
{
    "token": "",
    "kf_url": "",
    "kc_url": ""
}
```

## Usage

```bash
# download media
python3 kobomedia.py --asset-uid agBMEh8GWxTrCSWQuWyE5d

# or
./kobomedia.py --asset-uid agBMEh8GWxTrCSWQuWyE5d
  
# or
kobomedia --asset-uid agBMEh8GWxTrCSWQuWyE5d
```

### Optional fields

- `limit`: Limit number of submissions per query, paginate until complete
- `query`: Set a custom query in the Mongo query syntax
- `chunk-size`: Set chunk size for saving data to files
- `throttle`: Control time between each download to reduce server strain
- `verbosity`: Control verbosity of stdout

```bash
./kobomedia.py --asset-uid agBMEh8GWxTrCSWQuWyE5d
  --limit 10 \
  --query '{"_submission_time": {"$gt": "2021-08-04"}}' \
  --chunk-size 2048 \
  --throttle 2
  --verbosity 2
```

## Output

Media downloads will be in the following directory structure:
```
{asset_uid}
├── {submission_uid}
│   ├── {filename}
│   └── {filename}
├── {submission_uid}
│   └── {filename}
├── {submission_uid}
│   └── {filename}
├── {submission_uid}
│   └── {filename}
└── {submission_uid}
    ├── {filename}
    └── {filename}
```
