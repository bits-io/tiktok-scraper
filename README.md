# FastAPI Project

Development in python v3.12g

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Requirements

This project requires the following dependencies:

- FastAPI==0.111.0
- uvicorn==0.30.1
- sqlalchemy==2.0.31
- alembic==1.13.1
- pydantic==2.7.4
- mysqlclient==2.2.4
- python-dotenv==1.0.1
- selenium==4.21.0
- beautifulsoup4==4.12.3
- python-jose==3.3.0
- pydantic-settings==2.3.3
- pymysql==1.1.1
- passlib==1.7.4
- bcrypt==4.1.3

## Installation

```bash
git clone https://github.com/iam-holding/tikify-scrapper.git
cd tikify-scrapper
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Database Migration

```bash
alembic init alembic
alembic upgrade head
```

## Project Structure

```bash
proyek/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── crud/
│   ├── db/
│   ├── models/
│   ├── schemas/
├── .env
├── alembic.ini
├── requirements.txt
├── README.md

```

## Testing

```bash
pytest
```

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (git checkout -b feature/awesome-feature)
3. Commit your changes (git commit -m 'Add some awesome feature')
4. Push to the branch (git push origin feature/awesome-feature)
5. Open a pull request

## License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
