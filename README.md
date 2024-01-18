# LSPD_Lovisetto_Kim


# **Car Rental Website:**
### Welcome to the Car Rental Website project! This web application allows car owners to upload information about their cars, and users can browse through the available cars and rent them for a specified period. The backend is built using Flask, and the frontend is designed using Bootstrap.

## **Table of Contents:**
##### Installation
##### Usage
##### Folder Structure
##### Database
##### Contributing
##### License
##### Installation
##### To run the Car Rental Website locally, follow these steps :

### **Clone the repository:**

bash
Copy code
git clone https://github.com/your-username/car-rental-website.git
Navigate to the project directory:

bash
Copy code
cd car-rental-website
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Usage
Run the application:

bash
Copy code
python main.py
Open your web browser and visit http://localhost:5000.

You can now explore the website, sign up, upload information about your car, and rent cars from other users.

### **Folder Structure**
Templates: Contains all the HTML files for the frontend pages.
Static: Contains all design-related files, utilizing Bootstrap for styling.
main.py: The main Python file for the Flask application.
forms.py: Contains classes with information about users and cars.
scss
Copy code
car-rental-website/
│
├── Templates/
│   ├── index.html
│   ├── upload_car.html
│   ├── view_cars.html
│   └── ... (other HTML files)
│
├── Static/
│   ├── style.css
│   ├── bootstrap.min.css
│   └── ... (other design-related files)
│
├── main.py
├── forms.py
└── requirements.txt

### **Database**
The main database for this project is named car.db. Make sure to manage your database and migrations appropriately as your application evolves.

### **Contributing**
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

### **License**
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code. Remember to include the original license text in your copy of the code.
