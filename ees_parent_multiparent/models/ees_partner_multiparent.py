# -*- coding: utf-8 -*-
# © 2017 Hideki Yamamoto
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools

class ees_partner_relation(models.Model):
	_name="ees_multiparent.relation"
	_rec_name = 'child_name'
	parent=fields.Many2one("res.partner",string="Company")
	parent_name=fields.Char(store=True, index=True, string="parent_name")
	child=fields.Many2one("res.partner",string="Contact")
	child_name=fields.Char(store=True, index=True, string="child_name")
	obsolete=fields.Boolean("Obsolete", default=False)
	role=fields.Char("Role")
	email=fields.Char("Email")
	phone=fields.Char("Tel")
	mobile=fields.Char("Cell")
	mailing=fields.Boolean("Posta SI")
	auth=fields.Boolean("Autorizzazione Comunicazione")
	address=fields.Char("Indirizzo")
	
	@api.onchange('parent')
	def ees_ensure_multiparent(self):
		if self.parent.email:
			self.email=self.parent.email
		if self.parent.phone:
			self.phone=self.parent.phone
		if self.parent.mobile:
			self.mobile=self.parent.mobile
		if self.child:
			if self.child.function:
				self.role=self.child.function
		self.parent_name=self.parent.name
	
	@api.multi
	def create(self,vals):
		sss = super(ees_partner_relation,self).create(vals)
		if(sss.child):
			fff=""
			xxx=""
			email=""
			phone=""
			mobile=""
			if sss.child:
				if sss.child.multiparents:
					ooo=sss.child.multiparents
					if ooo:
						for pp in ooo:
							fff=""
							if pp.obsolete!=True:
								if pp.role:
									if pp.parent_name:
										fff=fff+pp.role+" at "+pp.parent_name
									else:
										fff=fff+pp.role
								elif pp.parent_name:
										fff=fff+pp.parent_name
								if fff!="":
									fff="\n"+fff
								if pp.email:
									email=email+" "+pp.email
								if pp.phone:
									phone=phone+" "+pp.phone
								if pp.mobile:
									phone=mobile+" "+pp.mobile
								xxx=xxx+fff
					sss.child.email=email
					sss.child.phone=phone
					sss.child.mobile=mobile
			sss.child.allkan=xxx
		return sss
		
	@api.multi
	def unlink(self):
		if(self.child):
			fff=""
			xxx=""
			email=""
			phone=""
			mobile=""
			if self.child:
				if self.child.multiparents:
					ooo=self.child.multiparents
					if ooo:
						for pp in ooo:
							if pp.id!=self.id:
								if pp.obsolete!=True:
									fff=""
									if pp.role:
										if pp.parent_name:
											fff=fff+pp.role+" at "+pp.parent_name
										else:
											fff=fff+pp.role
									elif pp.parent_name:
											fff=fff+pp.parent_name
									if fff!="":
										fff="\n"+fff
									if pp.email!="":
										email=email+" "+pp.email
									if pp.phone!="":
										phone=phone+" "+pp.phone
									if pp.mobile!="":
										phone=mobile+" "+pp.mobile
									xxx=xxx+fff
						self.child.email=email
						self.child.phone=phone
						self.child.mobile=mobile
			self.child.allkan=xxx
		sss = super(ees_partner_relation,self).unlink()
		return sss
		
	@api.onchange('child')
	def ees_ensure_multichild(self):
		if self.child.email:
			self.email=self.child.email
		if self.child.phone:
			self.email=self.child.phone
		if self.child.function:
			self.role=self.child.function
		if self.child.mobile:
			self.mobile=self.child.mobile
		self.child_name=self.child.name
		
	def copy_from_parent(self):
		self.email=self.parent.email
		self.phone=self.parent.phone
		
	def copy_from_child(self):
		self.email=self.child.email
		self.phone=self.child.phone
		self.mobile=self.child.mobile
		
	def toggleobsolete(self):
		if self.obsolete:
			self.obsolete=False
		else:
			self.obsolete=True
	
	def togglemailing(self):
		if self.mailing:
			self.mailing=False
		else:
			self.mailing=True
	
	def toggleauth(self):
		if self.auth:
			self.auth=False
		else:
			self.auth=Truez

class ees_partner_multiparent(models.Model):
	_inherit='res.partner'
	multiparents=fields.One2many("ees_multiparent.relation","child",string="Companies")
	multichilds=fields.One2many("ees_multiparent.relation","parent",string="Contacts")
	multichild_ids=fields.Many2many(comodel_name="res.partner", relation="ees_multiparent_relation", column1="parent", column2="child", string="Impiegati")
	allkan=fields.Char(string="Relations")
	#multikan=fields.Char("multikan")
	
	#@api.multi
	#def ees_auto_kan(self):
	#	for record in self:
	#		fff=""
	#		xxx=""
	#		ooo=record.multiparents
	#		if ooo:
	#			for pp in ooo:
	#				fff=""
	#				if pp.obsolete!=True:
	#					if pp.role:
	#						if pp.parent_name:
	#							fff=fff+pp.role+" at "+pp.parent_name
	#						else:
	#							fff=fff+pp.role
	#					elif pp.parent_name:
	#							fff=fff+pp.parent_name
	#					if fff!="":
	#						fff="\n"+fff
	#					xxx=xxx+fff
	#		record.allkan=xxx
	#
	#@api.multi
	#def ees_preload_kanban(self,vals=False):
	#	fff=""
	#	xxx=""
	#	ooo=self.multiparents
	#	if vals:
	#		ooo=vals
	#	if ooo:
	#		for pp in ooo:
	#			fff=""
	#			if pp.role:
	#				if pp.parent_name:
	#					fff=fff+pp.role+" at "+pp.parent_name
	#				else:
	#					fff=fff+pp.role
	#			elif pp.parent_name:
	#					fff=fff+pp.parent_name
	#			if fff!="":
	#				fff="\n"+fff
	#			xxx=xxx+fff
	#	return xxx
	
	#@api.onchange('multiparents')
	#def ees_preload_kanban_save(self):
		#if self.multiparents:
		#	vals={}
		#	vals['allkan']=self.ees_preload_kanban()
		#	super(ees_partner_multiparent, self).write(vals)
		#	self.env.cr.commit()
			
	@api.multi
	def write(self,vals):
		#vals['allkan']=self.ees_preload_kanban()
		super(ees_partner_multiparent, self).write(vals)
		
	@api.onchange('parent_id')
	def ees_ensure_multiparent(self):
		doadd=True
		if self.parent_id:
			if self.multiparents:
				found=False
				for pp in self.multiparents:
					if pp.id==self.parent_id:
						found=True
				if found:
					doadd=False
			if doadd:
				rela=self.env['ees_multiparent.relation'].create({
					'parent':self.parent_id.id,
					'parent_name':self.parent_id.name,
					'child':self._origin.id,
					'child_name':self._origin.name,
					'active':True,
					'role':self.function,
					'phone':self.parent_id.phone,
					'email':self.parent_id.email
				})
				self.env.cr.commit()
