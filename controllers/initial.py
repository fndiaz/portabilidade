# coding=UTF-8
import os, commands

def principal():
	response.title = 'busca inteligente'

	form = SQLFORM.factory(
    	Field("data_inicio", "datetime", 
    	requires=IS_NOT_EMPTY(
    	error_message=T("não pode ser nulo"))),
    	Field("data_fim", "datetime", 
    	requires=IS_NOT_EMPTY(
    	error_message=T("não pode ser nulo"))),
    	Field('tipo', requires=IS_IN_SET(['Ligacoes', 'Consultas'], 
    	error_message=T("não pode ser nulo"))),
    	formstyle="divs",
    	submit_button='Pesquisar'
    		)

	if form.process().accepted:
		data_inicio = form.vars.data_inicio
		data_fim = form.vars.data_fim
		#data2 = ""+data+"%"
		session.data_inicio=data_inicio
		session.data_fim=data_fim
		if form.vars.tipo == 'Ligacoes':
			redirect(URL("initial", "/ligacoes"))
		elif form.vars.tipo == 'Consultas':
			redirect(URL("initial", "/consultas"))
	elif form.errors:
		response.flash="algo está errado"

	
	return response.render("initial/principal.html", form=form)

def ligacoes():
	response.title = 'ligacoes'
	session.func = 'ligacoes'
	#query = (db.log_portabilidade.data_port.like(session.data))
	query =	(db.log_portabilidade.data_port >= session.data_inicio) &\
			(db.log_portabilidade.data_port <= session.data_fim)

	db.log_portabilidade.id.readable=False
	grid = SQLFORM.grid(query=query,
		user_signature=True, searchable=True, csv=False, 
		paginate=50, details=False, orderby=~db.log_portabilidade.data_port)
	
	return response.render("initial/show_grid.html", grid=grid)

def consultas():
	response.title = 'consultas'
	session.func = 'consultas'
	#query = (db.portabilidade.data_port.like(session.data))
	query =	(db.portabilidade.data_port >= session.data_inicio) &\
			(db.portabilidade.data_port <= session.data_fim)
	print query

	db.portabilidade.id.readable=False
	grid = SQLFORM.grid(query=query,
		user_signature=True, searchable=True, csv=False, 
		paginate=50, details=False, orderby=~db.portabilidade.data_port)
	
	return response.render("initial/show_grid.html", grid=grid)

def get_json():
	#data= "'"+ session.data +"'"
	print 'json'

	if session.func == 'ligacoes':
		#consulta =db.executesql("SELECT o.nome_ope, p.operadora, COUNT( * ) FROM log_portabilidade p INNER JOIN portabilidade_operadora o ON o.id = p.operadora WHERE p.data_port LIKE %s GROUP BY o.nome_ope" %(data))
		query	= 	(db.log_portabilidade.data_port >= session.data_inicio) &\
					(db.log_portabilidade.data_port <= session.data_fim) &\
					(db.portabilidade_operadora.id == db.log_portabilidade.operadora)
		count 	=	db.portabilidade_operadora.nome_ope.count()
		con 	=	db(query).select(db.log_portabilidade.operadora, \
						db.portabilidade_operadora.nome_ope, count, \
						groupby=db.portabilidade_operadora.nome_ope)
		#print con
		#for dado in con:
		#	print dado.portabilidade_operadora.nome_ope
		#	print dado._extra[count]
	elif session.func == 'consultas':
		#consulta =db.executesql("SELECT nome_operadora, cod_operadora, COUNT( * ) FROM portabilidade WHERE data_port LIKE %s GROUP BY nome_operadora" %(data))
		query 	= 	(db.portabilidade.data_port >= session.data_inicio) &\
					(db.portabilidade.data_port <= session.data_fim)
		count 	= 	db.portabilidade.nome_operadora.count()
		con 	= 	db(query).select(db.portabilidade.nome_operadora, count,\
						groupby=db.portabilidade.nome_operadora)

	colunas = [{"label":"Operadora","type":"string"},
			{"label":"Quantidade","type":"number"}]
	linhas=[]
	for dado in con:
		if session.func == 'ligacoes':
			linhas.append({"c":[{"v":dado.portabilidade_operadora.nome_ope},{"v":dado._extra[count]}]})
		elif session.func == 'consultas':
			linhas.append({"c":[{"v":dado.portabilidade.nome_operadora},{"v":dado._extra[count]}]})

	final ={"rows" : linhas, "cols" : colunas}

	return response.json(final)

def blacklist():
	db.port_blacklist.id.readable=False

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
