import mysql.connector

datab= mysql.connector.connect(
            host="localhost",
            user="root", #write your user
            password="", #write your password
            database="interactive_bot", #write your database_name
)
mycursor= datab.cursor()

if mycursor:
    print("connected")
else:
    print("fail connected")


#insert data
def insertData(account_name, text_content, ordered):
    sql = "INSERT INTO data_tbl (account_name, text_content, ordered) VALUES (%s, %s, %s)"
    val= (account_name,text_content, ordered)
    mycursor.execute(sql,val)
    datab.commit()



#get data
# def selectData():
#    sql= "SELECT * FROM data_tbl "
#    mycusor.excute(sql)
#    res= mycusor.fetchall()
#    for i in res:
#        print(i)

insertData('Kim Duc BT','An chot','1')



