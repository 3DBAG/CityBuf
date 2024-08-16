printf "==3BAG\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/3DBAG.city.jsonl' '/Users/ravi/git/paper_cjseq/data/3DBAG.cb'

# wildly inconssistent attribute types on the same attribute, some attributes are always null (how to determine type?)
printf "==3DBV\n"
python cjseq2cb.py /Users/ravi/git/paper_cjseq/data/3DBV.city.jsonl /Users/ravi/git/paper_cjseq/data/3DBV.cb --schema eindregistratie:bool,objectid:int,objecteindtijd:bool,relatievehoogteligging:float,p_punt_datum:bool

# JSON attribute values
printf "==Helsinki\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Helsinki.city.jsonl' '/Users/ravi/git/paper_cjseq/data/Helsinki.cb'

# Textures (not yet supported)
# python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Helsinki_tex.city.jsonl' '/Users/ravi/git/paper_cjseq/data/Helsinki_tex.cb'

# MultiLineString
printf "==Ingolstadt\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Ingolstadt.city.jsonl' '/Users/ravi/git/paper_cjseq/data/Ingolstadt.cb'

# no CRS defined, no attributes
printf "==Montréal\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Montréal.city.jsonl' '/Users/ravi/git/paper_cjseq/data/Montréal.cb'

printf "==NYC\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/NYC.jsonl' '/Users/ravi/git/paper_cjseq/data/NYC.cb'

# has geometry instances (not yet supported)
# python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Railway.city.jsonl' '/Users/ravi/git/paper_cjseq/data/Railway.cb'

printf "==Rotterdam\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Rotterdam.jsonl' '/Users/ravi/git/paper_cjseq/data/Rotterdam.cb'

printf "==Vienna\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Vienna.city.jsonl' '/Users/ravi/git/paper_cjseq/data/Vienna.cb'

printf "==Zurich\n"
python cjseq2cb.py '/Users/ravi/git/paper_cjseq/data/Zurich.city.jsonl' '/Users/ravi/git/paper_cjseq/data/Zurich.cb'