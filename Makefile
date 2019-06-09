SHELL = /bin/bash

##
# Definitions.

stub :=
space := $(stub) $(stub)
scr_space := $(stub)\ $(stub)

ERROR_OFFSET = 100
ERROR_HEALTHCHECK = $((${ERROR_OFFSET} + 1))

.SUFFIXES:

PACKAGE_NAME = shiftd
PACKAGE_VERSION = 0.1.0

ADDIN_SCRIPT = $(PACKAGE_NAME).py
ADDIN_MANIFEST = $(PACKAGE_NAME).manifest

srcdir = $(CURDIR)/$(PACKAGE_NAME)
builddir = $(CURDIR)/build
distdir = $(CURDIR)/dist
docdir = $(CURDIR)/doc
autodocdir = $(docdir)/autodoc

## OS specifics.

ifneq ($(shell which lsb_release 2>/dev/null),)
	OS_ID = $(shell lsb_release -is)
	OS_CODENAME = $(shell lsb_release -cs)
endif

## Platform-related definitions.

PLATFORM = $(shell uname -s)

ifeq (${PLATFORM},Darwin)
	AUTODESK_PATH = ${HOME}/Library/Application\ Support/Autodesk
	FUSION_SITE_PACKAGES = ${HOME}/Applications/Autodesk\ Fusion\ 360.app/Contents/Api/Python/packages:
	FUSION_ADDINS = $(AUTODESK_PATH)/Autodesk\ Fusion\ 360/API/AddIns
endif

ifneq ($(findstring MINGW64_NT,${PLATFORM}),)
	AUTODESK_PATH = /c/Documents\ and\ Settings/Administrator/AppData/Local/Autodesk/
	FUSION_SITE_PACKAGES = $(shell find $(AUTODESK_PATH)/webdeploy/production -name Api -type d | tr '\n' ':')
	FUSION_ADDINS = /c/Users/Administrator/AppData/Roaming/Autodesk/Autodesk\ Fusion\ 360/API/AddIns
endif

## Tools.

tools =

ifeq ($(shell uname -s),Darwin)
	SED = gsed
else
	SED = sed
endif

ifeq ($(shell which ${SED} 2>/dev/null),)
	tools += $(SED)
endif

GREPTOOL = ack
ifeq ($(shell which ${GREPTOOL} 2>/dev/null),)
    GREPTOOL = egrep
endif

AWK = awk
ifeq ($(shell which ${AWK} 2>/dev/null),)
    tools += $(AWK)
endif

DOCKER = $(shell which docker 2>/dev/null)

## Virtual environment.

VENV_DIR = $(CURDIR)/.venv

VENV = virtualenv
ifeq ($(shell which ${VENV} 2>/dev/null),)
	tools += $(VENV)
endif

## Docker.

PYTHON_VERSION = 3.7
DOCKER_BASE_IMAGE = python:$(PYTHON_VERSION)

DOCKER_PS_ARGS = -s
DOCKER_WORK_DIR = /usr/local/lib/python$(PYTHON_VERSION)/site-packages/$(PACKAGE_NAME)

DOCKER_PORT = 8088

## Documentation.

doctools =

SPHINX_BUILDDIR = $(docdir)/_build
SPHINX_STATIC = $(docdir)/_static
SPHINX_TEMPLATES = $(docdir)/_templates

SPHINX_OPTS = -d $(SPHINX_BUILDDIR)/doctrees $(CURDIR)/doc

SPHINX = sphinx-build
ifeq ($(shell which ${SPHINX} 2>/dev/null),)
	doctools += $(SPHINX)
endif

SPHINX_APIDOC = sphinx-apidoc
ifeq ($(shell which ${SPHINX_APIDOC} 2>/dev/null),)
	doctools += $(SPHINX_APIDOC)
endif

AUTODOC_EXCLUDE_MODULES =

PDFLATEX = pdflatex
ifeq ($(shell which ${PDFLATEX} 2>/dev/null),)
	doctools += $(PDFLATEX)
endif


##
# All

all: healthcheck sys-post-defs
ifdef tools
	$(error Can't find tools:${tools})
endif
ifeq (${DOCKER},)
	$(warning Can't find Docker executable)
endif

	@echo "AUTODESK_PATH -> $(AUTODESK_PATH)"
	@echo "FUSION_SITE_PACKAGES -> $(FUSION_SITE_PACKAGES)"
	@echo "FUSION_ADDINS -> $(FUSION_ADDINS)"

ifndef AUTODESK_PATH
	$(error Undefined variable: AUTODESK_PATH)
endif
ifndef FUSION_SITE_PACKAGES
	$(error Undefined variable: FUSION_SITE_PACKAGES)
endif
ifndef FUSION_ADDINS
	$(error Undefined variable: FUSION_ADDINS)
endif

.PHONY: sys-post-defs
sys-post-defs:
	$(eval FUSION_SITE_PACKAGES = ${FUSION_SITE_PACKAGES::=})
ifneq ($(findstring MINGW64_NT,${PLATFORM}),)
	$(eval FUSION_SITE_PACKAGES = ${FUSION_SITE_PACKAGES}/Python/packages)
	$(eval FUSION_SITE_PACKAGES := $(subst ${space},${scr_space},${FUSION_SITE_PACKAGES}))
endif


##
# Virtual environment.

.PHONY: requirements
# target: requirements – Compile Pip requirements
requirements:
	@if [[ ! -f requirements.txt ]]; then \
		touch requirements.txt; \
	fi
	@$(DOCKER) run -it --rm \
		-v "$(CURDIR)/requirements.in:/requirements.in" \
		-v "$(CURDIR)/requirements.txt:/requirements.txt" \
	"$(DOCKER_BASE_IMAGE)" "$(SHELL)" -c \
		'pip install pip-tools && CUSTOM_COMPILE_COMMAND="make requirements" \
		pip-compile -o requirements.tmp /requirements.in && \
		cat requirements.tmp > requirements.txt'

$(VENV_DIR): requirements.txt requirements-test.txt
	@$(VENV) -p "python$(PYTHON_VERSION)" "$(VENV_DIR)"
	@"$(VENV_DIR)/bin"/pip install -U setuptools pip
	@"$(VENV_DIR)/bin"/pip install -Ur $<
	@"$(VENV_DIR)/bin"/pip install -Ur $(word 2,$^)

.PHONY: venv
# target: venv – Create the virtual environment
venv: $(VENV_DIR)


##
# Docker

.PHONY: docker-info
# target: docker-info - Display system-wide information
docker-info:
	@echo
	@$(DOCKER) info
	@echo

.PHONY: docker-stats
# target: docker-stats - Show all images and containers
docker-stats:
	@echo
	@$(DOCKER) images -a
	@echo
	@$(DOCKER) ps -a
	@echo

.PHONY: docker-statsall
# target: docker-statsall - Same as `stats`, but more details provided
docker-statsall:
	@echo
	@$(DOCKER) images -a
	@echo
	@$(DOCKER) ps -a $(DOCKER_PS_ARGS)
	@echo

.PHONY: docker-build
# target: docker-build - Build image from scratch
docker-build: distclean dist
	@$(DOCKER) build \
		-f "$(CURDIR)/Dockerfile" -t "$(PACKAGE_NAME):$(PACKAGE_VERSION)" \
		--no-cache .

.PHONY: docker-run
# target: docker-run - Run temporary container in an interactive mode
docker-run:
	@$(DOCKER) run -it --rm -p "$(DOCKER_PORT):$(DOCKER_PORT)" \
		"$(PACKAGE_NAME):$(PACKAGE_VERSION)"

.PHONY: docker-clean
# target: docker-clean – Clean dangling images
docker-clean:
	@$(DOCKER) rmi -f \
		$(shell $(DOCKER) images -a | $(GREPTOOL) "<none>" | $(AWK) '{print $$3}') \
	&>/dev/null || :

.PHONY: docker-distclean
# target: docker-distclean – Clean built containers
docker-distclean:
	@$(DOCKER) rm -f $(shell $(DOCKER) ps -aq) &>/dev/null || :

.PHONY: docker-mostlyclean
# target: docker-mostlyclean – Remove all unused images, built containers and volumes
docker-mostlyclean: docker-distclean
	@$(DOCKER) image prune -a
	@$(DOCKER) volume prune -f


##
# Building and packaging

.PHONY: dist
# target: dist – Create a binary (wheel) distribution
dist:
	@[ ! -f "$(distdir)"/*.whl ]
	@python setup.py bdist_wheel

.PHONY: sdist
# target: sdist – Create a source distribution
sdist:
	@[ ! -f "$(distdir)"/*.tar.gz ]
	@python setup.py sdist

.PHONY: install
# target: install – Install project sources in "development mode"
install:
	@python setup.py develop

.PHONY: uninstall
# target: uninstall – Uninstall project sources
uninstall:
	@python setup.py develop --uninstall


##
# Testing

.PHONY: check
# target: check – Run tests
check:
	@python setup.py test -a "-vv"


##
# Documentation.

.PHONY: doc
doc:
ifdef doctools
	$(error Can't find tools:${doctools})
endif

.PHONY: apidoc
# target: apidoc - Create one reST file with automodule directives per package
apidoc: doc
	@$(SPHINX_APIDOC) --force --private -o "$(autodocdir)" $(PACKAGE_NAME) \
		$(foreach module,$(AUTODOC_EXCLUDE_MODULES),$(PACKAGE_NAME)/$(module))

.PHONY: html
# target: html – Render standalone HTML files
html: doc
	@$(SPHINX) -b html $(SPHINX_OPTS) "$(SPHINX_BUILDDIR)/html"

.PHONY: pdf
# target: pdf – Generate LaTeX files and run them through pdflatex
pdf: doc
	@$(SPHINX) -b latex $(SPHINX_OPTS) "$(SPHINX_BUILDDIR)/latex" && \
		$(MAKE) -C "$(SPHINX_BUILDDIR)/latex" all-pdf


##
# Deployment

.PHONY: healthcheck
# target: healthcheck – Health check Fusion's deploy
healthcheck:
	@echo -en "\nHealth checking Fusion's deploy..."

	$(eval deploys_number = \
	  $(shell echo "${FUSION_SITE_PACKAGES}" | $(AWK) -F":" '{print NF-1}'))
	@echo -n "$(deploys_number) "

	@if [[ $(deploys_number) -eq 1 ]]; then \
		echo "OK"; \
	else \
		echo "FAILED"; \
	fi

.PHONY: clean-site
# target: clean-site – Remove all packages from Fusion's site except builtins and clean temporary files
clean-site: sys-post-defs
	@echo -en "\nCleaning Fusion's site packages..."

	@find $(FUSION_SITE_PACKAGES) \
        -mindepth 1 -maxdepth 1 \
        -type d \
            -not -name adsk \
            -exec rm -rf {} + -o \
        \
        -type f -exec rm -rf {} + \
    && \
    find $(FUSION_SITE_PACKAGES) \
		-name "*.py[cod]" -exec rm -f {} + -o \
		-name __pycache__ -exec rm -rf {} + \
	&& \
    echo "DONE"

.PHONY: install-addin
# target: install-addin – Install addin to the Fusion's host
install-addin:
	@echo -e "\nInstalling addin: $(PACKAGE_NAME)..."
	$(eval addin_path = ${FUSION_ADDINS}/${PACKAGE_NAME})

	@if [[ ! -d $(addin_path) ]]; then \
		mkdir $(addin_path); \
	fi

	@for filename in $(ADDIN_SCRIPT) $(ADDIN_MANIFEST); do \
		echo -n "$${filename} "; \
		if [[ -f $(addin_path)/$${filename} ]]; then \
			echo "(SKIPPED)"; \
			continue; \
		fi; \
		cp $(srcdir)/$${filename} $(addin_path) && echo "(DONE)"; \
	done

.PHONY: remove-addin
# target: remove-addin – Remove addin from the Fusion's host
remove-addin:
	@echo -en "\nRemoving addin: $(PACKAGE_NAME)..."
	$(eval addin_path = ${FUSION_ADDINS}/${PACKAGE_NAME})

	@if [[ -d $(addin_path) ]]; then \
		rm -rf $(addin_path) && echo "DONE"; \
	else \
		echo "NOT FOUND"; \
	fi


##
# Auxiliary targets

.PHONY: help
# target: help – Display all callable targets
help:
	@echo
	@egrep "^\s*#\s*target\s*:\s*" [Mm]akefile \
	| $(SED) -r "s/^\s*#\s*target\s*:\s*//g"
	@echo

## Cleaners.

.PHONY: clean
# target: clean – Clean the project's directrory
clean:
	@find "$(CURDIR)" \
		-name "*.py[cod]" -exec rm -fv {} + -o \
		-name __pycache__ -exec rm -rfv {} +
	@rm -rfv \
		"$(CURDIR)/.cache" \
		"$(CURDIR)/.mypy_cache" \
		"$(CURDIR)/.pytest_cache"

.PHONY: distclean
# target: distclean – Clean the project's build output
distclean:
	@find "$(CURDIR)" -path "$(VENV_DIR)" -prune -o \
		-name "*.egg-info" -exec rm -rfv {} + -o \
		-name "*.dist-info" -exec rm -rfv {} +

	@rm -rfv \
		"$(CURDIR)/.eggs" \
		"$(builddir)" \
		"$(distdir)" \
		"$(SPHINX_BUILDDIR)" \
		"$(SPHINX_STATIC)" \
		"$(SPHINX_TEMPLATES)"
	@rm -fv "$(docdir)/autodoc"/*.rst

.PHONY: mostlyclean
# target: mostlyclean – Delete almost everything
mostlyclean: clean distclean
	@find "$(CURDIR)" -name .DS_Store -exec rm -fv {} +

	@rm -rfv \
		"$(VENV_DIR)"
