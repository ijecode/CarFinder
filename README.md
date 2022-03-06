# CarFinder
Scraper for popular used car websites, with notifications for new matching results

# Setup
Checkout the project, and from the root folder run:
    pip install -r requirements.txt

Complete the parameters file `parameters.yaml`. Run `carfinder\carfinder.py`. You will probably want to schedule this through a cron job or similar, depending on your operating system.

To 'start fresh', delete `carfinder\cars.db`. 

# Work in progress
Still to be addressed:
- eBay searching
- OS notifications
- Multiple parameter files
- Complete interrogation of the parameter file to stop errors
- More search criteria