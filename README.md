## Setup

```bash
git clone https://github.com/joshuaberetta/kobomedia
cd kobomedia

# optional
chmod +x kobomedia.py
sudo ln -s $(pwd)/kobomedia.py /usr/local/bin/kobomedia
```

## Usage

```bash
# download media
python3 kobomedia.py --url "https://kf.kobotoolbox.org/#/forms/aTQHSsjPsN5zWEofd9dKEb/summary" \
  --token your_secret_token

# or
./kobomedia.py --url "https://kf.kobotoolbox.org/#/forms/aTQHSsjPsN5zWEofd9dKEb/summary" \
  --token your_secret_token
```

### optional fields

- `limit`: Limit number or submission per query, paginate until complete
- `query`: Set a custom query in the Mongo query syntax
- `chunk-size`: Set chunk size for saving data to files
- `verbosity`: Control verbosity of stdout

```bash
./kobomedia.py --url "https://kf.kobotoolbox.org/#/forms/aTQHSsjPsN5zWEofd9dKEb/summary" \
  --token your_secret_token \
  --limit 10 \
  --query '{"_submission_time": {"$gt": "2021-08-04"}}' \
  --chunk-size 2048 \
  --verbosity 2
```
