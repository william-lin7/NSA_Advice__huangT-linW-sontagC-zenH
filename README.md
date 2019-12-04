# NSA_Advice__huangT-linW-sontagC-zenH

ROSTER
- Tyler Huang: Back end
- William Lin: Project Manager
- Coby Sontag: Back end
- Hilary Zen: Front end

WEBSITE
- An interface where users can enter their address to receive information
  regarding their surroundings.

APIs Used
- Google Civic Information: https://docs.google.com/document/d/1AYUhQ15IkV8yX_zLNDS0x9Q0l_QY6vOv3aA3f_LHDzU/edit
    - provides civic information based on residential address
- Google Places: https://docs.google.com/document/d/1zLgw_m5zhouRFc_Vm21_RTpCQwBbu_Cr2zOJH9VGL3o/edit
    - takes in location as latitude and longitude and returns places nearby
- Maps Embed: https://docs.google.com/document/d/1BrK8KIi1jxdETaGoEcuEB_UDiGwZhFFeWxZ_dlwiFww/edit
    - takes in location as latitude and longitude and returns a google map of it
- Location IQ: https://docs.google.com/document/d/1i6Zl1cfnEr_u9oqvk1XbwJWGMqf8Vp2IdQzUf2InGek/edit
    - returns the latitude and longitude of an address
- OpenWeatherMap: https://docs.google.com/document/d/1V-IRbvKGQpJMTfYxsOcew8A-9y9otnKWGP7eXR2bJ6Y/edit
    - provides weather data given geographic location

<br><br>
**HOW TO RUN THE PROJECT**
<br>Before you run: Download flask
- from home directory
```
$ python3 -m venv [insert hero]                          #creates virtual environment
$ . hero/bin/activate                                    #activates virtual environment
(hero)$ pip install -r doc/requirements.txt              #installs all required packages
(hero)$ deactivate                                       #deactivates the virtual environment (do after you finish testing)
```

Running the project:
1. Clone the repository
```
git clone [insert HTTPS url of repo]
```
2. Run the main python program (app.py)
```
python3 app.py
```
3. Copy and paste the local url into your browser
4. Reset everything
```
python3 reset.py
```
4. Register an account through the register button
5. Log in with your new account
6. Once you're logged in, follow the instructions on the website to create your API keys
7. Click update info to enter a city in the 'location' section
8. Enter an address in the 'address' section in the form
      '[address number] [street] [city]'
9. Now have fun! Explore our website and the random things we tell you based on your address.
