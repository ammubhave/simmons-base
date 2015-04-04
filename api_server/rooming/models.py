from django.db import models

class GRT(models.Model):
    section_name = models.CharField(max_length=10, unique=True)
    min_freshmen_doubles = models.IntegerField()
    def __unicode__(self):
        return "ID: "+str(self.id) + " " + self.section_name

    def filled(self):
        grt_rooms = self.room_set.all()
        num_in_grt = len(grt_rooms)
        num_already_in_grt = len([x for x in grt_rooms if x.full()])
        return num_already_in_grt >= num_in_grt - self.min_freshmen_doubles

class Room(models.Model):
    number = models.CharField(max_length=5, unique = True)
    max_occupancy = models.IntegerField()
    grt_section = models.ForeignKey(GRT)

    def type(self):
        if self.max_occupancy == 1:
            return "single"
        elif self.max_occupancy == 2:
            return "double"

    def check(self):
        num_occupants = numResidents(self)
        if num_occupants > self.max_occupancy:
            return (False, "Too many occupants for "+self.type())
        return (True, "Success")

    def available(self):
        return not self.grt_section.filled() and not self.full()

    def empty(self):
        return self.num_occupants() == 0
    
    def full(self):
        return self.num_occupants() == self.max_occupancy

    def num_occupants(self):
        return len(self.resident_set.all())
        
    def __unicode__(self):
        return "Room "+ self.number

class Resident(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    athena = models.CharField(max_length=20, unique=True)
    year = models.IntegerField(default=0)
    room = models.ForeignKey(Room)

    def __unicode__(self):
        return self.first_name + self.last_name + "(" + self.athena + ")"

