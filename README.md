<div align="center">

<h3 align="center">TekniMicro</h3>
  <a href="./LICENCE">
    <img alt="License" src="https://img.shields.io/badge/Licence-MIT-green?style=for-the-badge" />
  </a>
  <a href="https://www.repostatus.org/#active">
    <img alt="Project Status: Active" src="https://img.shields.io/badge/Project%20Status-Active-brightgreen?style=for-the-badge" />
  </a>
</div>

---

## 📝 Table of Contents
- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Built Using](#built_using)
- [Authors](#authors)

## 🧐 About <a name = "about"></a>
Integrates microcontroller* powered NeoPixel LED strips with the [TeknIoT](https://gitlab.com/tekniot/) project.

\* *Currently only ESP8266 is tested*

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites
This install guide assumes that you have Python installed locally and your micro controller is running [MicroPython](http://micropython.org/) with WebREPL enabled.

### Installing
First, install all required development dependencies:
```shell
pip install -r requirements.txt
```

## 🚀 Deployment <a name = "deployment"></a>
First copy  `.env.template` to `.env` and set the hostname, password and port for WebREPL.

Now you're ready to deploy the codebase to your micro controller. The first time, it will ask for configuration details, like the WiFi SSID and MQTT hostname. These values will be persisted in `src/config.json`.
```shell
sh deploy.sh
```

## ⛏️ Built Using <a name = "built_using"></a>
- [MicroPython](https://micropython.org/) - High Level Programming Language for Microcontrollers
- [MQTT](https://mqtt.org/) - Backend Communication Protocol
- [Gitlab](https://gitlab.com) - VCS

## ✍️ Authors <a name = "authors"></a>
- [Adriaan Knapen](https://aknapen.nl) [![Addono@Gitlab](https://img.shields.io/badge/Gitlab-@Addono-orange?style=for-the-badge&logo=gitlab)](https://gitlab.com/Addono) [![Addono@Github](https://img.shields.io/badge/Github-@Addono-black?style=for-the-badge&logo=github)](https://github.com/Addono)