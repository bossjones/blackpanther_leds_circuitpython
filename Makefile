# -*- coding: utf-8 -*-
#
# This Makefile is a dev-ops tool set.
# Compatible with:
#
# - Windows
# - MacOS
# - MacOS + pyenv + pyenv-virtualenv tool set
# - Linux

##########################################################################################
# What do @, - and + do as prefixes to recipe lines in Make?
# SOURCE: https://stackoverflow.com/questions/3477292/what-do-and-do-as-prefixes-to-recipe-lines-in-make
# @ suppresses the normal 'echo' of the command that is executed.
# - means ignore the exit status of the command that is executed (normally, a non-zero exit status would stop that part of the build).
# + means 'execute this command under make -n' (or 'make -t' or 'make -q') when commands are not normally executed. See also the POSIX specification for make and also §9.3 of the GNU Make manual.
##########################################################################################

# http://misc.flogisoft.com/bash/tip_colors_and_formatting

RED=\033[0;31m
GREEN=\033[0;32m
ORNG=\033[38;5;214m
BLUE=\033[38;5;81m
NC=\033[0m

export RED
export GREEN
export NC
export ORNG
export BLUE

# DEVICENAME := /dev/tty.usbmodem14101
DEVICENAME := $(shell ls /dev/tty.*| grep "tty.usbmodem" | awk '{print $1}')
BAUD_RATE := 115200

# verify that certain variables have been defined off the bat
check_defined = \
	$(foreach 1,$1,$(__check_defined))
__check_defined = \
	$(if $(value $1),, \
	  $(error Undefined $1$(if $(value 2), ($(strip $2)))))

list_allowed_args := side_to_render


list-serial-devices: ## ** List serial devices connected to laptop
	ls /dev/tty.*

connect-to-repl: ## ** Start gnu screen session to connect to repl
	screen $(DEVICENAME) $(BAUD_RATE)

repl: connect-to-repl ## ** (ALIAS) Start gnu screen session to connect to repl

debug: ## ** Dump Makefile vars to stdout
	@echo "DEVICENAME $(DEVICENAME)"
	@echo "BAUD_RATE $(BAUD_RATE)"

cp-screenrc: ## ** Copy .screenrc config from contrib folder to ~/.screenrc
	cp ./contrib/.screenrc ~/.screenrc

cp-to-device: ## ** Copy all code that we use to run our blackpanther suit to the adafruit microcontroller
	rsync --verbose --update nonblocking_timer.py /Volumes/CIRCUITPY/
	rsync --verbose --update left_chest.py /Volumes/CIRCUITPY/
	rsync --verbose --update buttonwatcher.py /Volumes/CIRCUITPY/
	rsync --verbose --update demorunner.py /Volumes/CIRCUITPY/
	rsync --verbose --update helloworld.py /Volumes/CIRCUITPY/
	rsync --verbose --update debugger.py /Volumes/CIRCUITPY/
	rsync --verbose --update nightlight.py /Volumes/CIRCUITPY/
	rsync --verbose --update pixelanimator.py /Volumes/CIRCUITPY/
	rsync --verbose --update rainbowdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update blinkdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update simpledemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update animation_utils.py /Volumes/CIRCUITPY/
	rsync --verbose --update code.py /Volumes/CIRCUITPY/
	@df -H /Volumes/CIRCUITPY/

rm-device: ## ** Remove all code that we use to run our blackpanther suit on the adafruit microcontroller
	rm -fv /Volumes/CIRCUITPY/nonblocking_timer.py
	rm -fv /Volumes/CIRCUITPY/left_chest.py
	rm -fv /Volumes/CIRCUITPY/buttonwatcher.py
	rm -fv /Volumes/CIRCUITPY/demorunner.py
	rm -fv /Volumes/CIRCUITPY/helloworld.py
	rm -fv /Volumes/CIRCUITPY/debugger.py
	rm -fv /Volumes/CIRCUITPY/nightlight.py
	rm -fv /Volumes/CIRCUITPY/pixelanimator.py
	rm -fv /Volumes/CIRCUITPY/rainbowdemo.py
	rm -fv /Volumes/CIRCUITPY/blinkdemo.py
	rm -fv /Volumes/CIRCUITPY/animation_utils.py
	rm -fv /Volumes/CIRCUITPY/simpledemo.py

.PHONY: clean
clean: rm-device ## ** (ALIAS) Remove all code that we use to run our blackpanther suit on the adafruit microcontroller


left-cp-to-device: ## ** (LEFT CHEST) Copy all code that we use to run our blackpanther suit to the adafruit microcontroller
	rsync --verbose --update nonblocking_timer.py /Volumes/CIRCUITPY/
	rsync --verbose --update left_chest.py /Volumes/CIRCUITPY/
	rsync --verbose --update buttonwatcher.py /Volumes/CIRCUITPY/
	rsync --verbose --update demorunner.py /Volumes/CIRCUITPY/
	rsync --verbose --update helloworld.py /Volumes/CIRCUITPY/
	rsync --verbose --update debugger.py /Volumes/CIRCUITPY/
	rsync --verbose --update nightlight.py /Volumes/CIRCUITPY/
	rsync --verbose --update pixelanimator.py /Volumes/CIRCUITPY/
	rsync --verbose --update rainbowdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update blinkdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update simpledemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update animation_utils.py /Volumes/CIRCUITPY/
	rsync --verbose --update code.py /Volumes/CIRCUITPY/
	@df -H /Volumes/CIRCUITPY/

right-cp-to-device: ## ** (RIGHT CHEST) Copy all code that we use to run our blackpanther suit to the adafruit microcontroller
	rsync --verbose --update nonblocking_timer.py /Volumes/CIRCUITPY/
	rsync --verbose --update right_chest.py /Volumes/CIRCUITPY/
	rsync --verbose --update buttonwatcher.py /Volumes/CIRCUITPY/
	rsync --verbose --update demorunner.py /Volumes/CIRCUITPY/
	rsync --verbose --update helloworld.py /Volumes/CIRCUITPY/
	rsync --verbose --update debugger.py /Volumes/CIRCUITPY/
	rsync --verbose --update nightlight.py /Volumes/CIRCUITPY/
	rsync --verbose --update pixelanimator.py /Volumes/CIRCUITPY/
	rsync --verbose --update rainbowdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update blinkdemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update simpledemo.py /Volumes/CIRCUITPY/
	rsync --verbose --update animation_utils.py /Volumes/CIRCUITPY/
	rsync --verbose --update code.py /Volumes/CIRCUITPY/
	@df -H /Volumes/CIRCUITPY/

render-demorunner-left: ## ** (LEFT CHEST) render demorunner.py using jinja2 templates for adafruit microcontroller
	jinja2 \
	-D render_left=True \
	$(PROJECT_ROOT_DIR)/demorunner.py.j2 > demorunner-left.py

render-demorunner-right: ## ** (RIGHT CHEST) render demorunner.py using jinja2 templates for adafruit microcontroller
	jinja2 \
	-D render_right=True \
	$(PROJECT_ROOT_DIR)/demorunner.py.j2 > demorunner-right.py

#######################
# How to create a local virtualenv to use with this Makefile, install deps like pytest, pylint, black, isort, autopep8, etc
# SOURCE: https://github.com/alanfranz/docker-rpm-builder/blob/v1dev/Makefile
#######################

# .PHONY: test integrationtest testexample clean distclean cleanexample install increase_minor_version upgrade freeze

# PYTHON ?= $(shell which python)
# VIRTUALENV ?= $(shell which virtualenv) -p $(PYTHON)
# SHELL := $(shell which bash)
# SRC_ROOT = drb
# FIND := $(shell which gfind || which find)

# info:
# 	@echo "DEVICENAME $(DEVICENAME)"
# 	@echo "BAUD_RATE $(BAUD_RATE)"
# 	@echo "PYTHON $(PYTHON)"
# 	@echo "VIRTUALENV $(VIRTUALENV)"
# 	@echo "SHELL $(SHELL)"
# 	@echo "SRC_ROOT $(SRC_ROOT)"
# 	@echo "FIND $(FIND)"

###########################################################
# Pyenv initilization - 12/23/2018 -- START
# SOURCE: https://github.com/MacHu-GWU/learn_datasette-project/blob/120b45363aa63bdffe2f1933cf2d4e20bb6cbdb8/make/python_env.mk
###########################################################

#--- User Defined Variable ---
PACKAGE_NAME="blackpanther_leds_circuitpython"

# Python version Used for Development
PY_VER_MAJOR="3"
PY_VER_MINOR="6"
PY_VER_MICRO="5"

#  Other Python Version You Want to Test With
# (Only useful when you use tox locally)
# TEST_PY_VER3="3.4.6"
# TEST_PY_VER4="3.5.3"
# TEST_PY_VER5="3.6.2"

# If you use pyenv-virtualenv, set to "Y"
USE_PYENV="Y"

#--- Derive Other Variable ---

# Virtualenv Name
VENV_NAME="${PACKAGE_NAME}3"

# Project Root Directory
GIT_ROOT_DIR=${shell git rev-parse --show-toplevel}
PROJECT_ROOT_DIR=${shell pwd}

ifeq (${OS}, Windows_NT)
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname -s)
endif


# ---------

# Windows
ifeq (${DETECTED_OS}, Windows)
    USE_PYENV="N"

    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/Scripts"
    SITE_PACKAGES="${VENV_DIR_REAL}/Lib/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/Lib64/site-packages"

    GLOBAL_PYTHON="/c/Python${PY_VER_MAJOR}${PY_VER_MINOR}/python.exe"
    OPEN_COMMAND="start"
endif


# MacOS
ifeq (${DETECTED_OS}, Darwin)

ifeq ($(USE_PYENV), "Y")
    VENV_DIR_REAL="${HOME}/.pyenv/versions/${PY_VERSION}/envs/${VENV_NAME}"
    VENV_DIR_LINK="${HOME}/.pyenv/versions/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
else
    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    VENV_DIR_LINK="./${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
endif

    GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
    OPEN_COMMAND="open"
endif


# Linux
ifeq (${DETECTED_OS}, Linux)
    USE_PYENV="N"

    VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    VENV_DIR_LINK="${PROJECT_ROOT_DIR}/${VENV_NAME}"
    BIN_DIR="${VENV_DIR_REAL}/bin"
    SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
    SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"

    GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
    OPEN_COMMAND="open"
endif


BASH_PROFILE_FILE = "${HOME}/.bash_profile"

BIN_ACTIVATE="${BIN_DIR}/activate"
BIN_PYTHON="${BIN_DIR}/python"
BIN_PIP="${BIN_DIR}/pip"
BIN_ISORT="${BIN_DIR}/isort"
# BIN_PYTEST="${BIN_DIR}/pytest"
# BIN_SPHINX_START="${BIN_DIR}/sphinx-quickstart"
# BIN_TWINE="${BIN_DIR}/twine"
# BIN_TOX="${BIN_DIR}/tox"
# BIN_JUPYTER="${BIN_DIR}/jupyter"

PY_VERSION="${PY_VER_MAJOR}.${PY_VER_MINOR}.${PY_VER_MICRO}"

.PHONY: help
help: ## ** Show this help message
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#--- Make Commands ---
.PHONY: info
info: ## ** Show information about python, pip in this environment
	@printf "Info:\n"
	@printf "=======================================\n"
	@printf "$$GREEN venv:$$NC                               ${VENV_DIR_REAL}\n"
	@printf "$$GREEN python executable:$$NC                  ${BIN_PYTHON}\n"
	@printf "$$GREEN pip executable:$$NC                     ${BIN_PIP}\n"
	@printf "$$GREEN site-packages:$$NC                      ${SITE_PACKAGES}\n"
	@printf "$$GREEN site-packages64:$$NC                    ${SITE_PACKAGES64}\n"
	@printf "$$GREEN venv-dir-real:$$NC                      ${VENV_DIR_REAL}\n"
	@printf "$$GREEN venv-dir-link:$$NC                      ${VENV_DIR_LINK}\n"
	@printf "$$GREEN venv-bin-dir:$$NC                       ${BIN_DIR}\n"
	@printf "$$GREEN bash-profile-file:$$NC                  ${BASH_PROFILE_FILE}\n"
	@printf "$$GREEN bash-activate:$$NC                      ${BIN_ACTIVATE}\n"
	@printf "$$GREEN bin-python:$$NC                         ${BIN_PYTHON}\n"
	@printf "$$GREEN bin-isort:$$NC                          ${BIN_ISORT}\n"
	@printf "$$GREEN py-version:$$NC                         ${PY_VERSION}\n"
	@printf "$$GREEN use-pyenv:$$NC                          ${USE_PYENV}\n"
	@printf "$$GREEN venv-name:$$NC                          ${VENV_NAME}\n"
	@printf "$$GREEN git-root-dir:$$NC                       ${GIT_ROOT_DIR}\n"
	@printf "$$GREEN project-root-dir:$$NC                   ${PROJECT_ROOT_DIR}\n"
	@printf "\n"

#--- Virtualenv ---
.PHONY: brew_install_pyenv
brew_install_pyenv: ## Install pyenv and pyenv-virtualenv
	-brew install pyenv
	-brew install pyenv-virtualenv

.PHONY: setup_pyenv
setup_pyenv: brew_install_pyenv enable_pyenv ## Do some pre-setup for pyenv and pyenv-virtualenv
	pyenv install ${PY_VERSION} -s
	pyenv rehash

.PHONY: init_venv
init_venv: ## Initiate Virtual Environment
ifeq (${USE_PYENV}, "Y")
	# Install pyenv
	#-brew install pyenv
	#-brew install pyenv-virtualenv

	# # Edit Config File
	# if ! grep -q 'export PYENV_ROOT="$$HOME/.pyenv"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'export PYENV_ROOT="$$HOME/.pyenv"' >> "${BASH_PROFILE_FILE}" ;\
	# fi
	# if ! grep -q 'export PATH="$$PYENV_ROOT/bin:$$PATH"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'export PATH="$$PYENV_ROOT/bin:$$PATH"' >> "${BASH_PROFILE_FILE}" ;\
	# fi
	# if ! grep -q 'eval "$$(pyenv init -)"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'eval "$$(pyenv init -)"' >> "${BASH_PROFILE_FILE}" ;\
	# fi
	# if ! grep -q 'eval "$$(pyenv virtualenv-init -)"' "${BASH_PROFILE_FILE}" ; then\
	#     echo 'eval "$$(pyenv virtualenv-init -)"' >> "${BASH_PROFILE_FILE}" ;\
	# fi

	# pyenv install ${PY_VERSION} -s
	# pyenv rehash

	-pyenv virtualenv ${PY_VERSION} ${VENV_NAME}
	@printf "FINISHED:\n"
	@printf "=======================================\n"
	@printf "$$GREEN Run to activate virtualenv:$$NC                               pyenv activate ${VENV_NAME}\n"
else
	virtualenv -p ${GLOBAL_PYTHON} ${VENV_NAME}
endif


.PHONY: up
up: init_venv ## ** Set Up the Virtual Environment


.PHONY: clean_venv
clean_venv: ## ** Clean Up Virtual Environment
ifeq (${USE_PYENV}, "Y")
	-pyenv uninstall -f ${VENV_NAME}
else
	test -r ${VENV_DIR_REAL} || echo "DIR exists: ${VENV_DIR_REAL}" || rm -rv ${VENV_DIR_REAL}
endif


#--- Install ---

.PHONY: uninstall
uninstall: ## ** Uninstall This Package
	# -${BIN_PIP} uninstall -y ${PACKAGE_NAME}
	-${BIN_PIP} uninstall -y requirements.txt

.PHONY: install
install: uninstall ## ** Install This Package via setup.py
	${BIN_PIP} install -r requirements.txt

.PHONY: dev_dep
dev_dep: ## Install Development Dependencies
	( \
		cd ${PROJECT_ROOT_DIR}; \
		${BIN_PIP} install -r requirements.txt; \
	)

# Frequently used make command:
#
# - make up
# - make clean
# - make install
# - make test
# - make tox
# - make build_doc
# - make view_doc
# - make deploy_doc
# - make reformat
# - make publish

###########################################################
# Pyenv initilization - 12/23/2018 -- END
# SOURCE: https://github.com/MacHu-GWU/learn_datasette-project/blob/120b45363aa63bdffe2f1933cf2d4e20bb6cbdb8/make/python_env.mk
###########################################################

# devenv: setup.py requirements.txt
# 	test -r devenv/bin/activate || $(VIRTUALENV) devenv || rm -rf devenv
# 	touch -t 197001011200 devenv
# 	source devenv/bin/activate && python devenv/bin/pip install -r requirements.txt && python devenv/bin/pip install --editable . --no-deps && python devenv/bin/pip check
# 	touch devenv

# # WARNING: this will freeze the CURRENT DEVELOPMENT ENVIRONMENT. Think twice if you've tinkered with it.
# freeze: devenv
# 	source devenv/bin/activate && python devenv/bin/pip freeze | grep -v "docker-rpm-builder" > requirements.txt

# upgrade: devenv
# 	source devenv/bin/activate && python devenv/bin/pip install --editable . --upgrade

# test: devenv
# 	devenv/bin/python -m unittest discover -v
# 	$(FIND) $(SRC_ROOT) -type f -name '*.py' | { ! xargs grep -H $$'\t' ; } || { echo 'found tabs in some py file' ; exit 1 ; }
