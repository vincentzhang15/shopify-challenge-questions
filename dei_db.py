import mysql.connector
from dbconn import dbconn

def get_next_imageid():
    db = dbconn()
    cursor = db.cursor()
    cursor.execute("select `id` from deitableids where `name`='deiimages'")
    rowid = 0
    result = cursor.fetchall()
    for x in result:
        rowid = x[0]+1
        break
    cursor.close()
    cursor = db.cursor()
    if rowid == 0:
        cursor.execute("insert into deitableids (`name`, `id`) values ('deiimages', 1)")
    else:
        cursor.execute("update deitableids set `id`=" + str(rowid) + " where `name`='deiimages'")
    db.commit()
    return rowid


def insert_image(values, tags, access):
    db = dbconn()
    cursor = db.cursor()
    cursor.execute("insert into deiimages (id, name, prop, content, userid, magic) values (%s, %s, %s, %s, %s, %s)", values)
    db.commit()
    images = []
    images += [{'id':values[0],'name':values[1],'tags':tags,'access':access,'content':values[3], 'userid':values[4]}]
    return images

def get_tagid(tag):
    db = dbconn()
    cursor = db.cursor()
    values=[]
    values+=[tag]
    cursor.execute("select id from deitags where name = %s", values)
    tagid = -1
    result = cursor.fetchall()
    for x in result:
        tagid = x[0]
        break
    cursor.close()
    return tagid

def insert_tag(tag):
    db = dbconn()
    cursor = db.cursor()
    values=[]
    values+=[tag]
    cursor.execute("insert into deitags (name) values (%s)", values)
    db.commit()
    return get_tagid(tag)

def insert_image_tag(imageid, tag):
    tagid = get_tagid(tag)
    if tagid == -1:
        tagid = insert_tag(tag)
    if tagid == -1:
        return
    values = [imageid, tagid]
    try:
        db = dbconn()
        cursor = db.cursor()
        cursor.execute("insert into deiimagetags (imageid, tagid) values (%s, %s)", values)
        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def upload_image_file(img,name,tags,access):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not img:
        return "No image", []

    if not img.content_type.startswith('image/'):
        return "Error file type", []

    ext = img.content_type[6:]

    if len(ext)<1:
        return "Error file type", []

    imageid = get_next_imageid()

    imagepath = "/tmp/images/"
    filename = imagepath + "image."+str(imageid)+"."+ext
    
    print("..... image filename .....  ", filename)

    import io
    try:
        with io.open(filename, "wb") as out:
            print(" open file done")
            image = img.read();
            print(" read done")
            out.write(image);
            print(" write done")
            out.close();
    except IOError as err:
        print("write file err = ", err)
        return str(err), []
        # raise        
    prop = (0,1)[access == "private"]

    print('Uploaded file:', img.filename, " contentType:", img.content_type, " id:", imageid, "  name:",name, " tags:", tags, "  access:", access, "prop:", prop)
    #values = []
    #values += [imageid]
    #values += [name]
    #values += [prop]
    #values += [img.content_type]
    userid = 'default'
    magic = '.'
    images = insert_image([imageid, name, prop, img.content_type, userid, magic], tags, access)
    for rawtag in tags.split(','):
        tag = rawtag.strip()
        if len(tag)>0:
            insert_image_tag(imageid, tag)
    return "", images

def get_random_images():
    db = dbconn()
    cursor = db.cursor()
    cursor.execute("select id, name, prop, content,userid, last_updated from deiimages order by RAND() limit 10")
    result = cursor.fetchall()
    images = {}
    for x in result:
        images[x[0]] = {'id':x[0],'name':x[1],'prop':x[2],'content':x[3], 'userid':x[4], 'updated':x[5]}
    cursor.close()
    return images

def get_image_tags(images):
    if len(images) == 0:
      return images
    print("get_image_tags for x in images) images = ", images)
    sql = "select imageid,tagid,name from deiimagetags left join deitags on tagid=id where imageid in "
    i = 0
    values = []
    for x in images:
        sql += ('(',',')[i!=0] + '%s'
        i = i + 1
        print("get_image_tags for x in images) x = ", x)
        values += [x]
    sql += ')'
    print("get_image_tags: sql=", sql)    

    db = dbconn()
    cursor = db.cursor()
    cursor.execute(sql, values)
    result = cursor.fetchall()
    tags = {}
    for x in result:
        if x[0] not in tags.keys():
            tags[x[0]] = x[2]
        else:
            tags[x[0]] += ',' + x[2]
    cursor.close()
    print("get_image_tags: tags=", tags)

    for x in images:
        images[x]['tags'] = tags[x]
    print("get_image_tags: images=", images)
    return images
