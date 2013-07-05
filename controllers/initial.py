# coding=UTF-8

def principal():
	response.title = 'busca inteligente'

	form = SQLFORM.factory(
    	Field("data", "date", 
    	requires=IS_NOT_EMPTY(
    	error_message=T("não pode ser nulo"))),
    	Field('tipo', requires=IS_IN_SET(['Global', 'Externa'], 
    	error_message=T("não pode ser nulo"))),
    	formstyle="divs",
    		)

	if form.process().accepted:
		data = form.vars.data
		data2 = ""+data+"%"
		session.data=data2
		if form.vars.tipo == 'Global':
			redirect(URL("initial", "/ligacoes"))
		elif form.vars.tipo == 'Externa':
			redirect(URL("initial", "/consultas"))
	
	return response.render("initial/principal.html", form=form)

def ligacoes():
	response.title = 'ligacoes'
	session.func = 'ligacoes'
	query = (db.log_portabilidade.data_port.like(session.data))

	db.log_portabilidade.id.readable=False
	grid = SQLFORM.grid(query=query,
		user_signature=True, searchable=True, csv=False, 
		paginate=50, details=False)
	
	return response.render("initial/show_grid.html", grid=grid)

def consultas():
	response.title = 'consultas'
	session.func = 'consultas'
	query = (db.portabilidade.data_port.like(session.data))

	db.portabilidade.id.readable=False
	grid = SQLFORM.grid(query=query,
		user_signature=True, searchable=True, csv=False, 
		paginate=50, details=False)
	
	return response.render("initial/show_grid.html", grid=grid)

def get_json():
	data= "'"+ session.data +"'"

	if session.func == 'ligacoes':
		consulta =db.executesql("SELECT o.nome_ope, p.operadora, COUNT( * ) FROM log_portabilidade p INNER JOIN portabilidade_operadora o ON o.id = p.operadora WHERE p.data_port LIKE %s GROUP BY o.nome_ope" %(data))
	elif session.func == 'consultas':
		consulta =db.executesql("SELECT nome_operadora, cod_operadora, COUNT( * ) FROM portabilidade WHERE data_port LIKE %s GROUP BY nome_operadora" %(data))

	colunas = [{"label":"Operadora","type":"string"},
			{"label":"Quantidade","type":"number"}]
	linhas=[]
	for row in consulta:
		linhas.append({"c":[{"v":row[0]},{"v":row[2]}]})

	final ={"rows" : linhas, "cols" : colunas}

	return response.json(final)

def blacklist():
	grid = SQLFORM.grid(Blacklist,
		user_signature=False, searchable=True, create=True, csv=False, 
		paginate=50, details=False)
	
	return response.render("initial/show_grid2.html", grid=grid)




def user():
	#if request.args(0) == 'register':
    #    	db.auth_user.bio.writable = db.auth_user.bio.readable = False
	return response.render("initial/user.html", user=auth())

def register():
	return auth.register()

def login():
        return auth.login()

def account():
    return dict(register=auth.register(),
                login=auth.login())
	
def download():
	return response.download(request, db)
