# Import Modules
from Classes import Profile as prf

# Initialize the constructor
bot = prf.Profile()

# Process automation
bot.GoTo()
bot.login()
bot.swipeRight()

# Close Chromedriver instance and executable
bot.driver.close()
bot.driver.quit()
