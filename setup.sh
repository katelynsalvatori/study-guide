#!/bin/bash

dropdb study_guide
createdb study_guide
psql study_guide < schema
