#!/usr/bin/env python

import wiringpi
from time import sleep
from neo4j.v1 import GraphDatabase

PIN_TO_SENSE = 3
driver = GraphDatabase.driver("bolt+routing://192.168.178.100:7687" )
#driver = GraphDatabase.driver("bolt://192.168.178.100:7687")

print "driver init done."

def add_node(tx):
    tx.run("create ()")

def count_nodes(tx):
    print "counting"
    return tx.run("match (n) return count(n) as c").single()[0]

def gpio_callback_2():
    print "GPIO_CALLBACK write!"
    with driver.session() as session:
        session.write_transaction(add_node)

def gpio_callback_3():
    print "GPIO_CALLBACK read!"
    with driver.session() as session:
        print "session"
        count = session.read_transaction(count_nodes)
        print "we have %d nodes" % (count)

wiringpi.wiringPiSetupGpio()
#wiringpi.pinMode(PIN_TO_SENSE, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(2, wiringpi.GPIO.PUD_UP)
wiringpi.pullUpDnControl(3, wiringpi.GPIO.PUD_UP)


wiringpi.wiringPiISR(2, wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_2)
wiringpi.wiringPiISR(3, wiringpi.GPIO.INT_EDGE_FALLING, gpio_callback_3)

while True:
    wiringpi.delay(2000)
