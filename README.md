# Create environment

```
python3.12 -m venv venv
. ./venv/bin/activate
```

# Install requirements

```
pip install -r requirements.txt
```

# Initialize Database

```
flask init-db
```

# Run application

```
flask --app app.py run
```

# CREATE SYSTEMD SERVICE


Copy the essdata.service to /etc/systemd/system/ (you need root privileges)

Note: You need to change paths and environment variables according your preferences

Now in order to install de service, you need to run the next command as root

```
systemctl daemon-reload
systemctl start essdata.service
systemctl enable essdata.service
```
