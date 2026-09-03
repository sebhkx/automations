# automations

## Scripts
### a4-a5-duplex-booklet (Simulate duplex for single sided printer)
- Ensure packages are installed
  `python3 -m pip install pypdf`
  
```
python a4_to_a5_booklet.py input.pdf
```

## Browser bot
### router-clients (Log in and get name and IP of all connected clients)
- .env
  `pip install python-dotenv`
- playwright
  `python -m playwright install chromium`