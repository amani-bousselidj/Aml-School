class GeneralSettings:
    def __init__(self):
        self.site_name = "Your Site Name"
        self.phone = "123-456-7890"
        self.email = "example@example.com"
        self.facebook = "https://facebook.com/yourpage"
        self.twitter = "https://twitter.com/yourpage"
        # Add other settings here

    def update_settings(self, data):
        # Update settings from form data or other sources
        self.site_name = data.get('site_name', self.site_name)
        self.phone = data.get('phone', self.phone)
        self.email = data.get('email', self.email)
        # Update other settings

# Initialize the settings object
general_settings = GeneralSettings()
