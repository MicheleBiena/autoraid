<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/MicheleBiena/autoraid">
    <img src="program.png" alt="Program" width="1200" height="640">
  </a>
<h3 align="center">AUTORAID</h3>

  <p align="center">
    Python bot to auto-host Pokémon Scarlet and Violet Tera Raids, based on sysbot-base by olliz0r.
    <br />
    <a href="https://github.com/MicheleBiena/autoraid"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/MicheleBiena/autoraid/issues">Report Bug</a>
    ·
    <a href="https://github.com/MicheleBiena/autoraid/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#built-with">Built with</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li>
      <a href="#roadmap">Roadmap</a>
    </li>
    <li>
      <a href="#contributing">Contributing</a>
    </li>
    <li>
      <a href="#contacts">Contacts</a>
    </li>
    <li>
      <a href="#credits">Credits</a>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built with

- [![Python][python.org]][python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

Install [sysbot-base](https://github.com/olliz0r/sys-botbase) and [ldn-mitm](https://github.com/spacemeowx2/ldn_mitm/releases/tag/v1.14.0) (required to control your switch when the game is closed) on your switch. Remember that ldn-mitm could block lan play, so read its github page carefully.

### Prerequisites

Install [Python](https://www.python.org/) and set its install location on PATH environment variable. (You can do it automatically while installing)

### Installing

1. Download the .zip file from the release page.

2. Run install.bat to install the dependencies. If you get an error check again your installation of Python and the content of the PATH. Remember to restart your PC after updating path.

3. Run autoraid.exe

4. Compile the settings, save and restart the program to make them valid.

### Building

1. Clone the repo
   ```sh
   git clone https://github.com/MicheleBiena/autoraid.git
   ```
2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. After setting up a raid on your switch (See Usage below) you can run autoraid_gui.py
   ```sh
   python .\Autoraid.Windows\autoraid_gui.py
   ```
4. Alternatively, you can build it using [pyinstaller](https://pypi.org/project/pyinstaller/) or [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/) with the --onedir option (--onefile is not supported for some of the libraries used). Remember to add CustomTkinter as a dependency, follow this [guide](https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging) to see how to do it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

1. Deactivate autosave on your game, and set text speed to Fast.
   If you're using any Edizon cheat remember to disable them during the game startup by keeping L pressed while selecting the game and the profile.

2. Find a Tera Raid that you would like to host, and stand in front of it.

3. Put a Pokémon that could be useful for the raid in front of your party.
   At the moment the bot will only select its first move and spam it,
   so prepare something that could win the raid (Like a Perrserker that spams Screech).

4. Make sure you're offline and right in front of the den, possibly in a place
   that can't be reached by wild Pokémon, so that when you press A the den opens.

5. Select from the program the desired options: ("preferential chats" and "snitch mode" are only applicable to the telegram integration. You can set up a list of chat ids that will receive the password 15 seconds before all othere ids, and with snitch mode before the raid starts a screenshot revealing the participants will be sent to all chat ids. Snitch mode can't be selected while preferential ids are enabled, so to not reveal which users have the advantage)

6. Click on Run Bot to start/stop the bot, the first thing it will do is connecting to the internet in game.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

### General

- [ ] Ban List for Abusers
- [ ] RaidCrawler Integration

### Telegram Integration

- [x] Priority Queue
- [x] Snitch Mode

### Aesthetic

- [x] GUI
- [x] executable file

See the [open issues](https://github.com/MicheleBiena/autoraid/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have an issue to report, please go to [open issues](https://github.com/MicheleBiena/autoraid/issues) and describe your problem. You may also add the log.txt from the bot session that encountered a problem to make it more clear.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contacts

michelebiena@gmail.com

Project Link: [https://github.com/MicheleBiena/autoraid](https://github.com/MicheleBiena/autoraid)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Credits

- [olliz0r](https://github.com/olliz0r/) for [Sysbot-base](https://github.com/olliz0r/sys-botbase), on which this program relies on
- [kwsch](https://github.com/kwsch), [Lusamine](https://github.com/Lusamine), [Archit Date](https://github.com/architdate), [LegoFigure11](https://github.com/LegoFigure11) and all those who contributed to [Sysbot.NET](https://github.com/kwsch/SysBot.NET) and [PkHex](https://github.com/kwsch/PKHeX) for all the ram byte offsets and pointer that make this bot possible.
- [jtszalay](https://github.com/jtszalay) for integration with non Windows machines.

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[haskell.org]: https://img.shields.io/badge/Haskell-Haskell.org-blueviolet
[haskell-gloss]: https://img.shields.io/badge/Haskell--Gloss-Gloss-blue
[haskell-url]: https://www.haskell.org/
[gloss-url]: https://hackage.haskell.org/package/gloss
[contributors-shield]: https://img.shields.io/github/contributors/MicheleBiena/autoraid.svg?style=for-the-badge
[contributors-url]: https://github.com/MicheleBiena/autoraid/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/MicheleBiena/autoraid.svg?style=for-the-badge
[forks-url]: https://github.com/MicheleBiena/autoraid/network/members
[stars-shield]: https://img.shields.io/github/stars/MicheleBiena/autoraid.svg?style=for-the-badge
[stars-url]: https://github.com/MicheleBiena/autoraid/stargazers
[issues-shield]: https://img.shields.io/github/issues/MicheleBiena/autoraid.svg?style=for-the-badge
[issues-url]: https://github.com/MicheleBiena/autoraid/issues
[license-shield]: https://img.shields.io/github/license/MicheleBiena/autoraid.svg?style=for-the-badge
[license-url]: https://github.com/MicheleBiena/autoraid/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[next-url]: https://nextjs.org/
[react.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[react-url]: https://reactjs.org/
[vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[vue-url]: https://vuejs.org/
[angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[angular-url]: https://angular.io/
[svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[svelte-url]: https://svelte.dev/
[laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[laravel-url]: https://laravel.com
[bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[bootstrap-url]: https://getbootstrap.com
[jquery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[jquery-url]: https://jquery.com
[python.org]: https://img.shields.io/badge/python-3.10.9-violet
[python-url]: https://www.python.org/
