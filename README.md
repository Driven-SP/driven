# Driven
Universal portal for all your addresses

## Vision 
Provide a universal address portal to the people who move to avoid conflicting addresses in different platforms and better track their mails and packages.
## Motivation 
Addresses are a crucial part of someone's identity and are a mode of communication for different services and platforms (like Banks, Healthcare, government, corportates) and the user. Usually when people move they have to change their address in a lot of such platforms and due to human or system errors there is always a high chance of address inconsistency between these platforms. This leads to problems like the mail or package being sent to a different or older address. This is a big problem and on top of that changing addresses manually in all these sites is a pain. We would like to automate this process by creating a universal portal for all your addresses. This is a one-stop-shop where you can change your address and provide an `address_id` to all the sites that require your address and then these sites will do an API call to the Driven DB to grab your most recent address.

Link to the design document: https://docs.google.com/document/d/18R_s3iGXKmfRXtoiz-nQf5x4ap4tq9QUMvOHO62qjVg/edit?usp=sharing

## Setup Instructions
Make sure you have python3 installed on your macbook.

Clone the repository and set it up. 
```
git clone https://github.com/Driven-SP/driven
cd Driven
pip3 install virtualenv
virtualenv --python=$(which python3) env
source activate.sh
pip3 install -r requirements.txt
flask run
```

## Testing Instructions
This project uses pytest which is installed as part of the requirements. Use the following command to run all tests:
```
pytest -v
```

To run tests in specific modules or directories, go to the directory and then use the above command.
