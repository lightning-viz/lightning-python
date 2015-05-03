#!/bin/bash

#setup travis-ci configuration basing one the being-built branch

if [[ $TRAVIS_BRANCH == 'master' ]] ; then
    export DEPLOY_HTML_DIR=docs
elif [[ $TRAVIS_BRANCH == 'develop' ]] ; then
    export DEPLOY_HTML_DIR=docs/develop
elif [[ $TRAVIS_BRANCH =~ ^v[0-9.]+$ ]]; then
    export DEPLOY_HTML_DIR=docs/${TRAVIS_BRANCH:1}
else
    export DEPLOY_HTML_DIR=docs/$TRAVIS_BRANCH
fi
