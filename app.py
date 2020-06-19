from flask import Response,request,Flask
from flask_cors import CORS
from urllib.parse import quote,urlencode
import json
app=Flask(__name__)
CORS(app,resorces={r'/*': {"origins": '*'}})
def parseRequest():
  args=request.args.to_dict()
  args.update(request.form)
  token=None
  if "token" in args:
    token=args.pop("token")
  return dict(token=token,args=args)
@app.route("/sign-in")
def login():
  args=parseRequest()["args"]
  return request_("auth/sign-in",None,args,"POST")
@app.route("/categories")
def categories():
  token=parseRequest()["token"]
  return request_("categories",token)
@app.route("/comics")
def comics():
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  if("favourites" in args):
    args.pop("favourites")
    return request_(f"users/favourite?"+urlencode(args),token=token)
  if("search" in args):
    args.pop("search")
    page=args.pop('page',1)
    return request_(f"comics/advanced-search?page={page}",token,dict(args),"POST")
  return request_("comics?"+urlencode(args),token)
@app.route("/comics/<bookId>")
def info(bookId):
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  return request_("comics/"+bookId,token=token)
@app.route("/comics/<bookId>/eps")
def episodes(bookId):
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  return request_(f"comics/{bookId}/eps?"+urlencode(args),token=token)
@app.route("/comics/<bookId>/like")
def like(bookId):
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  return request_(f"comics/{bookId}/like",token=token,method="POST")
@app.route("/comics/<bookId>/favourite")
def favourate(bookId):
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  return request_(f"comics/{bookId}/favourite",token=token,method="POST")
@app.route("/comics/<bookId>/<int:epId>/pages")
def pictures(bookId,epId):
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  image_quality=args.pop("quality","original")
  return request_(f"comics/{bookId}/order/{epId}/pages?"+urlencode(args),token=token,image_quality=image_quality)
@app.route("/keywords")
def keywords():
  token=parseRequest()["token"]
  return request_("keywords",token=token)
@app.route("/search")
def search():
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  page=args.pop("page")
  return request_(f"comics/advanced-search?page={page}",token,dict(args),"POST")
@app.route("/",methods=["POST","GET"])
def main():
  return parseRequest()
@app.route("/favourites")
def favourates():
  _x=parseRequest()
  token=_x["token"]
  args=_x["args"]
  return request_(f"users/favourite?"+urlencode(args),token=token)
if __name__=="__main__":
	app.run()