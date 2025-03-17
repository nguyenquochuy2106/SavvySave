# 📌 Phase 1: Planning & Design

## ✅ 1. Define Core Features
We are building **SavvySave**, a smart **Saving & Expense Tracking** app with **FaceID authentication**. The key features include:

### 🔹 Authentication
- User **sign-up and login** with FaceID or password.
- Secure authentication using **FaceNet** for FaceID.
- **JWT token-based authentication** for backend security.

### 🔹 Expense & Income Management
- Add, edit, delete **transactions** (income & expenses).
- Categorize transactions (e.g., Food, Rent, Salary).
- **Recurring transactions** (e.g., monthly bills, subscriptions).
- Store transaction history in **Amazon RDS**.

### 🔹 Savings Goal Planner
- Set **financial goals** (e.g., save $5000 in 6 months).
- Track progress with **visual insights**.
- Receive **reminders & suggestions** to reach savings goals.

### 🔹 Financial Insights & Analytics
- Generate **spending reports & visual charts**.
- Show **monthly and yearly savings trends**.
- Smart suggestions based on user spending behavior.

---

## ✅ 2. UI Wireframes & Design Planning
Before development, we need to **design wireframes** for key screens:

| Screen | Description |
|--------|------------|
| **Login Page** | FaceID & password login, register option. |
| **Dashboard** | Shows savings, expenses, and income overview. |
| **Transaction Page** | Add, edit, and delete transactions. |
| **Savings Goal Page** | Set and track savings goals. |
| **Analytics Page** | Spending trends, charts, and financial insights. |

---

## ✅ 3. Database Schema (ERD Design)
We need to define the **database tables** for **users, transactions, and savings goals**.

### 🔹 User Table (`users`)
| Column       | Type        | Description |
|-------------|------------|-------------|
| `id`        | UUID       | Unique user ID |
| `username`  | String     | Unique username |
| `email`     | String     | User's email (for login) |
| `password`  | String (hashed) | Encrypted password |
| `face_id_embedding` | JSON | FaceNet vector for FaceID |
| `created_at` | Timestamp | Account creation date |

### 🔹 Transactions Table (`transactions`)
| Column       | Type      | Description |
|-------------|----------|-------------|
| `id`        | UUID     | Unique transaction ID |
| `user_id`   | UUID     | Foreign key to `users` table |
| `amount`    | Decimal  | Transaction amount (+income, -expense) |
| `category`  | String   | (Food, Rent, Salary, etc.) |
| `date`      | DateTime | Date of transaction |
| `type`      | String   | `income` or `expense` |

### 🔹 Savings Goals Table (`savings_goals`)
| Column      | Type      | Description |
|------------|----------|-------------|
| `id`       | UUID     | Unique goal ID |
| `user_id`  | UUID     | Foreign key to `users` table |
| `target_amount` | Decimal | Goal savings amount |
| `current_savings` | Decimal | Current progress |
| `deadline` | Date     | Target completion date |

---

## ✅ 4. Tech Stack Finalization
| Component   | Technology |
|------------|------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend**  | Python, FastAPI |
| **Machine Learning** | FaceNet (for FaceID Authentication) |
| **Database** | Amazon RDS (PostgreSQL/MySQL) |

---

## 📌 Next Steps
1. **Confirm UI wireframes** – Do you need visual mockups?
2. **Finalize database schema** – Any extra fields needed?
3. **Prepare backend setup** – Set up FastAPI, database models.

🚀 Let’s move to **backend setup** next! 😊

