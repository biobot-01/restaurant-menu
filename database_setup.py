#!/usr/bin/env python3

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# Insert at E_O_F #
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
