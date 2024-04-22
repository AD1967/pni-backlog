from sqlalchemy import TEXT, Column, Date, DateTime, Float, ForeignKey, Text, Integer
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, TINYTEXT
from sqlalchemy.dialects.sqlite import INTEGER as SQLITE_INTEGER, TEXT as SQLITE_TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
from datetime import datetime
from sqlalchemy import func, cast
from . import db
import importlib

# класс для ошибок поиска в бд
class DbGetError(Exception):
    pass
# класс для ошибок добавления в бд
class DbPutError(Exception):
    pass

# класс для ошибок при добавлении конфигурации в бд
class DbPutError(Exception):
    pass


# контертер типов для sqlite
class MY_TINYINT(TypeDecorator):
    impl = TINYINT

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(SQLITE_INTEGER())
        else:
            return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value

# контертер типов для sqlite
class MY_TINYTEXT(TypeDecorator):
    impl = TINYTEXT

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(SQLITE_TEXT())
        else:
            return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value

# контертер типов для sqlite
class MY_INTEGER(TypeDecorator):
    impl = INTEGER(11)

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(SQLITE_INTEGER())
        else:
            return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value

def first_char_to_upper(str):
    return str[0].upper() + str[1:]

def get_elem_class_by_str(str):
    modulename, dot, _ = f"app.modules.db.model.{str}".rpartition('.')
    module = importlib.import_module(modulename)
    buf = getattr(module, str)
    return buf

# Базовый класс с доп функциями
class Base(db.Model):
    __abstract__  = True

    # инициализация свойств через словарь
    def init_by_dict(self, dict):
        for k, v in dict.items():
            setattr(self, k, v)
    # Класс модели в словарь
    def columns_to_dict(self):
        dict = {}
        for key in self.__mapper__.c.keys():
            dict[key] = getattr(self, key)
        return dict


# базовый класс для "элементов"
class BaseElement(Base):
    __abstract__  = True

    def __repr__(self):
        table_name =  getattr(self, "__tablename__")
        id =  "id_" + table_name
        return f"<{table_name} {id}>"

class Airheater(BaseElement):
    __tablename__ = 'airheater'

    id_airheater = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Convector(BaseElement):
    __tablename__ = 'convector'

    id_convector = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    power = Column(INTEGER(11))
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Crane(BaseElement):
    __tablename__ = 'crane'

    id_crane = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Door(BaseElement):
    __tablename__ = 'doors'

    id_door = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    R = Column(Float)
    beta = Column(Float)
    a = Column(Float)
    q = Column(Float)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Energoeff(BaseElement):
    __tablename__ = 'energoeff'

    id_energoeff = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    R = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Heatexchanger(BaseElement):
    __tablename__ = 'heatexchanger'

    id_heatexchanger = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    temp_min = Column(INTEGER(11))
    temp_max = Column(INTEGER(11))
    consumption = Column(INTEGER(11))
    power = Column(INTEGER(11))
    p_max = Column(INTEGER(11))
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Material(BaseElement):
    __tablename__ = 'material'

    id_material = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    coeff = Column(Float)
    capacity = Column(Float)
    density = Column(Float)
    thickness = Column(Float)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Period(BaseElement):
    __tablename__ = 'period'

    id_period = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    T = Column(INTEGER(11), nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Pipe(BaseElement):
    __tablename__ = 'pipe'

    id_pipe = Column(INTEGER(11), primary_key=True, unique=True)
    name = Column(Text, nullable=False)
    length = Column(INTEGER(11))
    diam = Column(INTEGER(11))
    temp = Column(INTEGER(11))
    Q = Column(INTEGER(11))
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Pump(BaseElement):
    __tablename__ = 'pump'

    id_pump = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    power = Column(INTEGER(11))
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Radiator(BaseElement):
    __tablename__ = 'radiator'

    id_radiator = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    power_section = Column(INTEGER(11))
    count_section = Column(INTEGER(11))
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Shutoffvalve(BaseElement):
    __tablename__ = 'shutoffvalve'

    id_shutoffvalve = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    diam = Column(INTEGER(11))
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Tempcontroller(BaseElement):
    __tablename__ = 'tempcontroller'

    id_tempcontroller = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    lambd = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class User(Base):
    __tablename__ = 'user'

    id_user = Column(INTEGER(11), primary_key=True)
    name = Column(MY_TINYTEXT, nullable=False)
    password = Column(Text, nullable=False)
    token = Column(TEXT, nullable=False)
    token_expiration  = Column(DateTime, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)
    def __repr__(self):
        return f"<User {self.id_user}>"

class Volume(BaseElement):
    __tablename__ = 'volume'

    id_volume = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    value = Column(Float, nullable=False)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Window(BaseElement):
    __tablename__ = 'window'

    id_window = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    R = Column(Float)
    a = Column(Float)
    q = Column(Float)

    def __init__(self, dict):
        self.init_by_dict(dict)

class Q_door(BaseElement):
    __tablename__ = 'Q_doors'

    id_q_doors = Column(INTEGER(11), primary_key=True)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)
    count_doors = Column(INTEGER(11), nullable=False)
    length_door = Column(Float, nullable=False)
    height_door = Column(Float, nullable=False)
    id_door = Column(ForeignKey('doors.id_door'), nullable=False, index=True)
    date_doors = Column(Date, nullable=False)

    build = relationship('Build')
    door = relationship('Door')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Q_wnd(BaseElement):
    __tablename__ = 'Q_wnd'

    id_q_wnd = Column(INTEGER(11), primary_key=True)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)
    count_windows = Column(INTEGER(11), nullable=False)
    length_wnd = Column(Float, nullable=False)
    height_wnd = Column(Float, nullable=False)
    id_window = Column(ForeignKey('window.id_window'), nullable=False, index=True)
    date_wnd = Column(Date, nullable=False)
        
    build = relationship('Build')
    window = relationship('Window')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Build(Base):
    __tablename__ = 'build'

    id_build = Column(INTEGER(11), primary_key=True)
    name = Column(Text, nullable=False)
    floors = Column(INTEGER(11), nullable=False)
    len_a = Column(Float, nullable=False)
    len_b = Column(Float, nullable=False)
    len_sum = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    date_build = Column(Date, nullable=False)
    id_user = Column(ForeignKey('user.id_user', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    temp_inside = Column(Float, nullable=False)
    temp_outside = Column(Float, nullable=False)

    user = relationship('User')

    def __init__(self, dict):
        self.init_by_dict(dict)
    def __repr__(self):
        return f"<Build {self.id_build}>"

class Q_construct_roof(BaseElement):
    __tablename__ = 'Q_construct_roof'

    id_q_construct_roof = Column(INTEGER(11), primary_key=True)
    constructs_energoeff = Column(ForeignKey('energoeff.id_energoeff'), nullable=False, index=True)
    roof_energoeff = Column(ForeignKey('energoeff.id_energoeff'), index=True)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)

    energoeff = relationship('Energoeff', primaryjoin='Q_construct_roof.constructs_energoeff == Energoeff.id_energoeff')
    build = relationship('Build')
    energoeff1 = relationship('Energoeff', primaryjoin='Q_construct_roof.roof_energoeff == Energoeff.id_energoeff')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Q_elec(BaseElement):
    __tablename__ = 'Q_elec'

    id_q_elec = Column(INTEGER(11), primary_key=True)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)
    elec_consumption_by_period = Column(Float)

    build = relationship('Build')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Q_floor(BaseElement):
    __tablename__ = 'Q_floor'

    id_q_floor = Column(INTEGER(11), primary_key=True)
    height_floor = Column(Float, nullable=False)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)

    build = relationship('Build')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Q_person(BaseElement):
    __tablename__ = 'Q_people'

    id_q_peoples = Column(INTEGER(11), primary_key=True)
    mens = Column(INTEGER(11), nullable=False)
    womens = Column(INTEGER(11), nullable=False)
    children = Column(INTEGER(11), nullable=False)
    time_average = Column(Float, nullable=False)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)

    build = relationship('Build')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Q_reheating(BaseElement):
    __tablename__ = 'Q_reheating'

    id_q_reheat = Column(INTEGER(11), primary_key=True)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)
    count_doors = Column(INTEGER(11), nullable=False)
    count_shkaf = Column(INTEGER(11), nullable=False)
    count_divan = Column(INTEGER(11), nullable=False)
    count_table = Column(INTEGER(11), nullable=False)
    count_shkafchik = Column(INTEGER(11), nullable=False)
    id_period = Column(INTEGER(11))
    walls_material = Column(ForeignKey('material.id_material'), nullable=False, index=True)
    floors_materials = Column(ForeignKey('material.id_material'), nullable=False, index=True)
    doors_material = Column(ForeignKey('material.id_material'), nullable=False, index=True)
    mebel_material = Column(ForeignKey('material.id_material'), nullable=False, index=True)
    divan_material = Column(ForeignKey('material.id_material'), nullable=False, index=True)
    table_material = Column(ForeignKey('material.id_material'), nullable=False, index=True)
    shkafchik_material = Column(ForeignKey('material.id_material'), nullable=False, index=True)

    divan_material_val = relationship('Material', primaryjoin='Q_reheating.divan_material == Material.id_material')
    doors_material_val = relationship('Material', primaryjoin='Q_reheating.doors_material == Material.id_material')
    floors_materials_val = relationship('Material', primaryjoin='Q_reheating.floors_materials == Material.id_material')
    build = relationship('Build')
    mebel_material_val = relationship('Material', primaryjoin='Q_reheating.mebel_material == Material.id_material')
    shkafchik_material_val = relationship('Material', primaryjoin='Q_reheating.shkafchik_material == Material.id_material')
    table_material_val = relationship('Material', primaryjoin='Q_reheating.table_material == Material.id_material')
    walls_material_val = relationship('Material', primaryjoin='Q_reheating.walls_material == Material.id_material')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Reliability(BaseElement):
    __tablename__ = 'reliability'

    id_reliability = Column(INTEGER(11), primary_key=True)
    id_build = Column(ForeignKey('build.id_build'), nullable=False, index=True)
    id_pipe = Column(ForeignKey('pipe.id_pipe'), nullable=False, index=True)
    id_radiator = Column(ForeignKey('radiator.id_radiator'), nullable=False, index=True)
    id_crane = Column(ForeignKey('crane.id_crane'), nullable=False, index=True)
    ihp = Column(MY_TINYINT(1))
    id_pump = Column(ForeignKey('pump.id_pump'), index=True)
    id_heatexchanger = Column(ForeignKey('heatexchanger.id_heatexchanger'), index=True)
    id_shutoffvalve = Column(ForeignKey('shutoffvalve.id_shutoffvalve'), nullable=False, index=True)
    ventsys = Column(MY_TINYINT(1))
    ascents_hws = Column(INTEGER(11))
    descents_hws = Column(INTEGER(11))
    count_crane = Column(INTEGER(11))
    ascents_heat = Column(INTEGER(11))
    descents_heat = Column(INTEGER(11))
    count_radiator = Column(INTEGER(11))

    build = relationship('Build')
    crane = relationship('Crane')
    heatexchanger = relationship('Heatexchanger')
    pipe = relationship('Pipe')
    pump = relationship('Pump')
    radiator = relationship('Radiator')
    shutoffvalve = relationship('Shutoffvalve')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Readings_vent(BaseElement):
    __tablename__ = 'readings_vent'

    id_reading = Column(INTEGER(11), primary_key=True)
    id_reliability = Column(ForeignKey('reliability.id_reliability'), nullable=False, index=True)
    value = Column(Float, nullable=False)

    reliability = relationship('Reliability')

    def __init__(self, dict):
        self.init_by_dict(dict)

class Weather(Base):
    __tablename__ = 'weather'
    Time = Column(DateTime, primary_key = True)
    T = Column(INTEGER(11))
    U = Column(INTEGER)
    DD = Column(TEXT)
    Ff = Column(INTEGER)
    c = Column(TEXT)
    def __init__(self, dict):
       self.init_by_dict(dict)
    def __repr__(self):
        return f"<Weather {self.Time}>"