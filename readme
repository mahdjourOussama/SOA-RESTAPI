# README - SOA Application for Loan Request Evaluation

## 📘 **Project Description**

This application was developed as part of the Master’s in Computer Science, specializing in DataScale at the University of Paris-Saclay. It implements a **Service-Oriented Architecture (SOA)** to process and evaluate loan requests.

The main objective is to demonstrate the benefits of SOA, such as modularity, component reusability, and service coordination via a RESTful orchestrator. The application simulates a loan evaluation process with autonomous, interconnected services.

---

## 📐 **Project Structure**

Here is the folder and file structure of the project:

```
├── .github/                 # CI/CD pipeline configuration (GitHub Actions)
├── data/                    # Dummy data for testing and simulation
├── db/                      # Simulations of external APIs (e.g., banking services)
├── services/                # Contains the microservice code and the user interface (via Streamlit)
│   ├── textmining/         # Information extraction service
│   ├── solvabilityVerification/   # Creditworthiness verification service
│   ├── properityEvaluation/         # Property evaluation service
│   └── decisionApproval/           # Final decision service
│   └── watchdog/           # service that watches for changes in data dir
│   └── serviceComposer/           # service that orchestrates all the other services
│   └── application/           # web interface built with Streamlit to enable file upload
├── tests/                   # Unit and integration test scripts
├── start.py                 # Entry point for starting the services
├── requirements.txt         # Dependencies for execution
├── requirements-dev.txt     # Development dependencies
└── README.md                # Project documentation (this file)
```

---

## ⚙️ **Main Services**

### 1️⃣ **Information Extraction Service**

- **Technology**: FastAPI
- **Objective**: Automatically extract essential information from loan requests.

### 2️⃣ **Creditworthiness Verification Service**

- **Technology**: FastAPI, Pandas
- **Objective**: Verify the client's creditworthiness by analyzing their financial data.

### 3️⃣ **Property Evaluation Service**

- **Technology**: FastAPI
- **Objective**: Evaluate the value of the properties to be financed

### 4️⃣ **Final Decision Service**

- **Technology**: FastAPI
- **Objective**: Make an automated decision on whether to approve or deny the loan.

These services are coordinated by a **RESTful orchestration module**, which manages the overall execution flow.

---

## 🚀 **Installation and Execution**

### **1️⃣ Clone the repository**

```bash
git clone https://github.com/mahdjourOussama/SOA-RESTAPI.git
cd SOA-RESTAPI
```

### **2️⃣ Install dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Start the services**

```bash
python start.py
```

The services are accessible via the URL: `http://localhost:8000`

---

## 📦 **Deployment with Docker**

### **1️⃣ Build Docker images**

```bash
docker-compose build
```

### **2️⃣ Start the containers**

```bash
docker-compose up
```

The services will then be available at `http://localhost:8000`.

---

## 🧪 **Tests**

The tests include **unit tests** for each microservice and **integration tests** to validate the global interaction of the services.

### **Run the tests**

```bash
python test/test.py
```

---

## 💡 **Main Challenges and Solutions**

| **Problem**             | **Solution**                         |
| ----------------------- | ------------------------------------ |
| Service synchronization | orchestration logic                  |
| Complex orchestration   | Central RESTful orchestration module |

---

## 📈 **Future Improvements**

- Integration with real external APIs.
- Implementation of fault tolerance mechanisms.

---

## 📋 **Contributors**

- **Student Name**: Oussama MAHDJOUR
- **University**: University of Paris-Saclay, Master in Computer Science Datascale
