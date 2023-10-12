# Coding challenges - JSON parser (Python)

Requirements before running
1. Python 3.10 or above

To install and run the tool

1. Clone the repo
2. Create a virtual environment using `venv`

Linux
```bash
python[3] -m venv .venv
```

Windows
```bash
py -m venv .venv
```
3. Activate the virtual environment using

**For Windows**

```bash
.venv\Scripts\activate
```

**For Linux**

```bash
source .venv/bin/activate
```

4. Install the dependencies (Optional: only use to format code and clean up imports)

```bash
pip install -r requirements.txt
```

5. Then you are free to run tests on any test file attached in the repo using

**For Windows**

```bash
py jparser.py \[Your filename here\]
```

**For Linux**

```bash
python[3] jparser.py \[Your filename here\]
```


## Progress marker
- [x] Step 1 - Basic empty JSON
- [x] Step 2 - Basic Single key pair
- [x] Step 3 - Multi key plus value types
- [x] Step 4 - Nested Objects, Nested Array types
- [ ] Step 5 - Additional test casing to cover official spec