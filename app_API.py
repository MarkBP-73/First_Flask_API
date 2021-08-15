# Import the Flask class form the flask module
from flask import Flask, render_template, redirect,url_for, request, session, flash, g, jsonify
from flask_restful import Resource, Api
from functools import wraps
import sqlite3

# create the application object based on Flask class
app= Flask(__name__)
api= Api(app)

# adds a variable to the app object which stores the database path.
app.database = "C:/sqlitedbs/disabilitysupport.db"

def connect_db():
    return sqlite3.connect(app.database)

#queries the database and returns a list of support for a specific study area.
def query_studyarea(studyArea):
    g.db = connect_db()
    curs = g.db.execute('select Tool_name, Summary, Features.feature_id from Features inner join Supports_study on Features.feature_id=Supports_study.feature_id where Supports_study.Study_difficulty_id= "%s"' % studyArea)
    results = [dict(tool=row[0],summary=row[1],id=row[2]) for row in curs.fetchall()]
    g.db.close()
    return results

#queries the database and returns a list of support for a specific study area.
def query_disability(disability):
    g.db = connect_db()
    curs = g.db.execute('select Features.feature_id, Tool_name, Summary from Features inner join Supports_disability on Features.feature_id=Supports_disability.feature_id where Supports_disability.disability_id= "%s"' % disability)
    results = [dict(tool=row[0],summary=row[1],id=row[2]) for row in curs.fetchall()]
    g.db.close()
    return results

def query_disability_area(disability,studyArea):
    g.db = connect_db()
    curs = g.db.execute('SELECT Features.feature_id, Tool_name, Summary FROM (Features INNER JOIN Supports_disability on Features.feature_id=Supports_disability.feature_id) INNER JOIN Supports_study ON Features.feature_id= Supports_study.feature_id WHERE (((Supports_disability.disability_id)= "%s") AND ((Supports_study.Study_difficulty_id)="%s"))' % (disability, studyArea))
    results = [dict(id=row[0],Tool=row[1],Feature=row[2]) for row in curs.fetchall()]
    g.db.close()
    return results


class SkillSupport(Resource):
    def get(self,area):
        return query_studyarea(area)

    def post(self):
        pass

class DisabilitySupport(Resource):
    def get(self,disability):
        return query_disability(disability)


    def post(self):
        pass

class DisabilityAreaSupport(Resource):
    def get(self,disability,area):
        return query_disability_area(disability,area)

    def post(self):
        pass



# map a url endpoint to the REST api.  This endpoint relates to area support is required.
# area variable can be Research, Academic_writing, Note_taking, Time_management, Access_to_technology
# Practical_off_campus_study, Examination_assessment, Social_interaction_communications, Travel_mobility
# Additional
api.add_resource(SkillSupport,"/support/<string:area>")

#map a url endpoint to the REST api.  This endpoint relates to the disability.
api.add_resource(DisabilitySupport,"/disability/<string:disability>")

#map a url endpoint to the REST api.  This endpoint relates to both disability and study studyArea
api.add_resource(DisabilityAreaSupport,"/disabilityarea/<string:disability>/<string:area>")



# start the server with the run() method
if __name__ =='__main__':
    app.run(debug=True)
