# Import core libanki functionality
from anki import Collection, template, find   # Note Collection here maps to collection and storage.Collection
from anki.utils import splitFields, joinFields
# import the main window object (mw) from ankiqt
from aqt import mw
# import the "show info",saveGeom,restoreGeom tools from utils.py
from aqt.utils import showInfo,saveGeom, restoreGeom
# import all of the Qt GUI library
from aqt.qt import *


def loadMainFrontend():
  mw.raDialog=mainFrontend(mw)

class mainFrontend(QDialog):
# Main frontend code is called by the menu click. Gets info from user and calls backend
  def __init__(self, win_parent = None):
    QDialog.__init__(self, win_parent)
    self.setWindowTitle("Replace all")    
    self.createWidgets()
  def createWidgets(self):    
    # Add model combo box & populate with all models
    self.label0=QLabel("Model")
    self.modelCombo=QComboBox()
    models=sorted(mw.col.models.allNames())    
    self.modelCombo.addItems(models)
    self.modelCombo.setCurrentIndex(0)
    # Add destination field combo box & set fields to populate based on model
    self.label1=QLabel("Destination Field")
    self.fieldCombo=QComboBox()
    fields=mw.col.models.fieldNames(mw.col.models.byName(models[0]))    
    self.fieldCombo.addItems(fields)   
    QObject.connect(self.modelCombo, SIGNAL("currentIndexChanged(const QString&)"), self.updateFieldList)
    # Add tag combo box
    self.label2=QLabel("Tag to limit to (optional)")
    self.tagCombo=QComboBox()
    allTags=sorted(mw.col.tags.all())
    allTags.insert(0,"")
    self.tagCombo.addItems(allTags)
    # Add text box for the user expression to fill
    self.label3=QLabel("Expression to fill")
    self.exprEdit=QLineEdit()
    # Add button to run script
    self.searchButton=QPushButton("Replace All")
    QObject.connect(self.searchButton, SIGNAL("clicked()"), self.buttonClicked)
    # Layout all above widgets in a vertical line
    self.vbox=QVBoxLayout()
    self.vbox.addWidget(self.label0)
    self.vbox.addWidget(self.modelCombo)
    self.vbox.addWidget(self.label1)
    self.vbox.addWidget(self.fieldCombo)
    self.vbox.addWidget(self.label2)
    self.vbox.addWidget(self.tagCombo)
    self.vbox.addWidget(self.label3)                        
    self.vbox.addWidget(self.exprEdit)
    self.vbox.addWidget(self.searchButton)
    self.setLayout(self.vbox)
    # Show the dialog
    self.show()     
  def buttonClicked(self):
    # Execute the backend code when the search button clicked
    modelName=self.modelCombo.currentText()
    destField=self.fieldCombo.currentText()
    tag=self.tagCombo.currentText()
    expr=self.exprEdit.displayText()
    numUpdates=mainBackend(modelName,tag,destField,expr)
    showInfo("%d notes were updated." % numUpdates)
            
  def updateFieldList(self,newIndex):
    # Repopulate the list of the fields when the model is changed
    m=mw.col.models.byName(newIndex)
    f=mw.col.models.fieldNames(m)
    self.fieldCombo.clear()
    self.fieldCombo.addItems(f)  
  
def mainBackend(modelName,tag,destField,expr):
# Main backend code called by the GUI to do the replace all/field fill operation 
  # Assign collection to col
  col=mw.col
  # Get the model id corresponding to modelName
  model=findModel(col,modelName)
  # Get the index belonging to destination field
  destFieldIdx=findFieldIdx(model,destField)
  # Run a database query and return list of noteid,fields of notes with specified model ID and tag
  noteid,tags,flds=fetchData(col,model,tag)
  # Render exp for each note
  newflds=[]
  for idx in range(len(flds)):
    flist=splitFields(flds[idx])
    fdic=makeFieldDic(col,model,flist)
    fdic['Tags'] = tags [idx]
    fdic['Type'] = model['name']
    flist[destFieldIdx]=template.render(expr,fdic)
    newflds.append([joinFields(flist),noteid[idx]])      
  # Write the new data to the database
  col.db.executemany("update notes set flds=? where id=?",newflds)
  # Return the number of notes which were updated
  return len(noteid)  

   
def findModel(col, val):
# Return the model from collection (col) corresponding to model name (val)             
  return col.models.byName(val)
    
def makeFieldDic(col,model,flist):
# Convert the fields list into a dictionary for use with template.render()
    fields = {}
    for (name, (idx, conf)) in col.models.fieldMap(model).items():
        fields[name] = flist[idx]
    return fields   

def findFieldIdx(model,fieldName):
# Return the index from model corresponding to fieldName
  fieldIdx=[]
  fieldName=fieldName.lower()
  for f in range(len(model['flds'])):
    if model['flds'][f]['name'].lower()==fieldName:
      fieldIdx.append(f)
  if len(fieldIdx)==1:
    return fieldIdx[0]
  elif len(fieldIdx)==0:
    raise NameError("Specified field \'" + fieldName + "\' not found")
  else:
    raise NameError("Specified field \'" + fieldName + "\' not unique")
    
def fetchData(col,model,tag):
  # Get all the notes with specified criteria
  if tag!='':
    nid=col.db.list("SELECT id FROM notes WHERE mid="+str(model['id'])+" AND tags LIKE \'% "+tag+" %\'")
    tags=col.db.list("SELECT tags FROM notes WHERE mid="+str(model['id'])+" AND tags LIKE \'% "+tag+" %\'")
    flds=col.db.list("SELECT flds FROM notes WHERE mid="+str(model['id'])+" AND tags LIKE \'% "+tag+" %\'")
  else:
    nid=col.db.list("SELECT id FROM notes WHERE mid="+str(model['id']))
    tags=col.db.list("SELECT tags FROM notes WHERE mid="+str(model['id']))
    flds=col.db.list("SELECT flds FROM notes WHERE mid="+str(model['id']))  
  return nid,tags,flds       
  

# create a new menu item, "Replace all"
action = QAction("Replace all", mw)
# set it to call loadMainFrontend() when it's clicked
mw.connect(action, SIGNAL("triggered()"),loadMainFrontend)
# and add it to the tools menu of main window
mw.form.menuTools.addAction(action)
#browser.Browser.Ui_Dialog.
