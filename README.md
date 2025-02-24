# BMC Server Setup Guide

## Prerequisites
Ensure you have the following:
- An AWS account
- A registered domain (optional, if you want to map your server to a domain)
- SSH client (e.g., OpenSSH, PuTTY)
- Git installed on your local machine
- Ngrok account

---

## Step 1: Create an AWS Account
1. Go to [AWS Console](https://aws.amazon.com/)
2. Sign up or log in to your AWS account
3. Complete identity verification and billing setup (if required)

---

## Step 2: Create an EC2 Instance
1. Open the **AWS Management Console**
2. Navigate to **EC2** > **Launch Instance**
3. Choose **Ubuntu 22.04 LTS** (or latest stable Ubuntu version)
4. Select an instance type (e.g., `t2.micro` for free tier)
5. Configure instance details:
   - Number of instances: `1`
   - Network: Default VPC (or create a new VPC if needed)
6. Add Storage:
   - 20GB SSD (recommended)
7. Configure security group:
   - Allow SSH (Port 22)
   - Allow HTTP (Port 80)
   - Allow custom TCP (Port 5000 for Flask, or any required ports)
8. Review and **Launch**
9. Create or select an existing **Key Pair** for SSH access

---

## Step 3: Connect to EC2 Instance
1. Open terminal (Linux/Mac) or use PuTTY (Windows)
2. Run the following command to connect via SSH:
   ```sh
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```
   (Replace `your-key.pem` with the key pair file and `your-ec2-public-ip` with the instance's public IP.)
3. Once connected, update and install dependencies:
   ```sh
   sudo apt update && sudo apt upgrade -y
   sudo apt install git python3 python3-pip -y
   ```

---

## Step 4: Allow Inbound Connections
1. Go to **AWS Console** → **EC2**
2. Select your **EC2 instance** → **Security Groups**
3. Click **Edit inbound rules**
4. Add rules:
   - **Custom TCP Rule:** Port `5000`, Source `0.0.0.0/0`
   - **Custom TCP Rule:** Port `4040` (for ngrok dashboard)
   - **HTTP (80):** Source `0.0.0.0/0`
   - **HTTPS (443):** Source `0.0.0.0/0`
   - **SSH (22):** Source `Your IP` for security
5. Save changes

---

## Step 5: Clone and Set Up the Repository
1. Navigate to the home directory:
   ```sh
   cd ~
   ```
2. Clone your BMC server repository:
   ```sh
   git clone https://github.com/YOUR_USERNAME/YOUR_BMC_REPO.git
   ```
3. Navigate to the project folder:
   ```sh
   cd YOUR_BMC_REPO
   ```
4. Install required Python packages:
   ```sh
   pip3 install -r requirements.txt
   ```

---

## Step 6: Run the Flask App
1. Navigate to the `api` folder:
   ```sh
   cd BMC_server/api
   ```
2. Run the Flask application:
   ```sh
   python3 app.py
   ```
3. The server will start on `http://127.0.0.1:5000`

---

## Step 7: Set Up Ngrok to Expose the Flask App
1. Install Ngrok (if not installed):
   ```sh
   curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null &&
   echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list &&
   sudo apt update && sudo apt install ngrok
   ```
2. Authenticate with Ngrok:
   ```sh
   ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN
   ```
   (Replace `YOUR_NGROK_AUTH_TOKEN` with your actual Ngrok token.)
3. Start Ngrok and expose port 5000:
   ```sh
   ngrok http 5000
   ```
4. Copy the **forwarding URL** from the terminal (e.g., `https://your-ngrok-url.ngrok-free.app`) and use it to access your API.

---

## Step 8: Test Your API
1. Use `curl` to test the API:
   ```sh
   curl -X POST "https://your-ngrok-url.ngrok-free.app/predict" -H "Content-Type: application/json" -d '{"customer_id":"LB-16795","keyword":"Printer"}'
   ```
2. If everything is working, your Flask app is successfully deployed!

---

## Step 9: Keep Flask App Running in Background (Optional)
To keep the Flask server running after you disconnect:
```sh
nohup python3 app.py > output.log 2>&1 &
```
To check logs:
```sh
cat output.log
```
To stop the Flask server:
```sh
ps aux | grep app.py
kill -9 PROCESS_ID
```

---

## Step 10: Auto-start Flask & Ngrok on Reboot (Optional)
To keep the Flask app and Ngrok running even after a reboot:
1. Open crontab editor:
   ```sh
   crontab -e
   ```
2. Add the following lines at the end:
   ```sh
   @reboot cd /home/ubuntu/YOUR_BMC_REPO/api && nohup python3 app.py > output.log 2>&1 &
   @reboot nohup ngrok http 5000 > /dev/null 2>&1 &
   ```
3. Save and exit.

---

## Conclusion
You have successfully set up your BMC server on AWS, deployed a Flask app, and exposed it using Ngrok. 🎉

For any issues, check logs and ensure security rules are configured correctly!

---

