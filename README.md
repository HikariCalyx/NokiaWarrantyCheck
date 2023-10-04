# Nokia Warranty Check
The warranty lookup system for Nokia phones manufactured by Triple-Color Company.

# Required Environment
Python 3.9.2 or newer. 

# Get Started
* Clone this repository.
* Edit ```warranty_api.py``` and replace both upstream_api_url and x_api_key into what you've found. For safety reason they cannot be disclosed publicly.
* Use pip to install all requirements:
> pip install -r requirements.txt
* Run main.py to host it over port 443. You may want to edit the port number and certificates if you don't want to protect it with SSL.

# Web Frontend
You can choose either host it via load balancer like Nginx, or host it via Flask template.
But if the API backend and frontend aren't at same domain, you'll have to add CORS configuration.

# Actual Website
https://warranty.hikaricalyx.com/
