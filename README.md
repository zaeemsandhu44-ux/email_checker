# 📧 Email Spam Checker

A machine learning-based **Email Spam Checker** built with Python and Flask.
The application analyzes an email/message and predicts whether it is **Spam** or **Not Spam** using a trained machine learning model.

## 🚀 Features

* 📩 Check whether an email is Spam or Not Spam
* 🤖 Machine Learning-based classification
* 🌐 Flask web application
* 🎨 Simple and user-friendly web interface
* 🧠 Pre-trained spam classification model
* 📊 Dataset included for model development
* 📝 Jupyter Notebook included for experimentation and training

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **Machine Learning**
* **Scikit-learn**
* **HTML**
* **CSS**
* **Jupyter Notebook**
* **Pickle**

## 📂 Project Structure

```text
email_checker/
│
├── model/
│   └── spam_classifier.pkl
│
├── static/
│   └── CSS / frontend files
│
├── templates/
│   └── HTML files
│
├── SMSSpamCollection
├── app.py
├── email.ipynb
├── email_subscription_demo.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/zaeemsandhu44-ux/email_checker.git
```

### 2. Open the Project

```bash
cd email_checker
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Required Libraries

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Start the Flask application:

```bash
python app.py
```

Then open the local URL shown by Flask in your browser.

Usually:

```text
http://127.0.0.1:5000/
```

## 🧠 How It Works

The basic workflow of the project is:

```text
User enters an email/message
          ↓
      Flask App
          ↓
   Text Processing
          ↓
 Machine Learning Model
          ↓
 Spam / Not Spam
          ↓
 Display Result
```

The trained model is stored as a `.pkl` file and is loaded by the Flask application to classify the submitted text.

## 📊 Dataset

The project includes the `SMSSpamCollection` dataset, which contains examples of spam and legitimate messages.

The dataset is used to train and evaluate the machine learning spam classifier.

## 🔮 Prediction

After entering an email or message, the application sends the text to the trained machine learning model.

The model returns a classification such as:

* **Spam** 🚨
* **Not Spam** ✅

## 📓 Jupyter Notebook

The project also includes:

```text
email.ipynb
```

The notebook can be used to understand the data preprocessing, model training, and machine learning workflow.

## 🎯 Purpose

This project was developed as a practical machine learning project to demonstrate how a trained classification model can be integrated into a web application using Flask.

## 👨‍💻 Author

**Muhammad Zaeem Nasir Sandhu**

GitHub:
https://github.com/zaeemsandhu44-ux

## 📄 License

This project is created for educational and learning purposes.
