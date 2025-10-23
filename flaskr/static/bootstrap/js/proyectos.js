import Service from './service.js';
import ComBsModal from './bs-modal.js';

const Matches = {
	template: `<div>
		<!--
		<form>
			<input type="text" class="form-control" placeholder="Buscar..." v-model="keyword" />
		</form>
		-->
		<table class="table table-sm table-striped">
		<thead>
		<tr>
			<th>Nro</th>
			<th>Proyecto</th>
			<th>Estado</th>
			<th>Fecha</th>
			<th></th>
		</tr>
		</thead>
		<tbody>
		<tr v-for="(match, i) in matches">
			<td>{{ i  + 1}}</td>
			<td>{{ match.nombre }}</td>
			<td>{{ match.estado }}</td>
			<td>{{ match.fecha_plazo_evaluacion }}</td>
			<td><button type="button" class="btn btn-sm btn-primary" v-on:click="assign(match)"><i class="fa fa-check"></i></button></td>
		</tr>
		</tbody>
		</table>
	</div>`,
	props: {
		matches: {type: Object, required: true, default: () => []},
	},
	data()
	{
		return {
			keyword: '',
		};
	},
	methods: 
	{
		assign(match)
		{
			this.$emit('assign', match);
		}
	},
	mounted()
	{
		console.log(this.matches);
	},
	created()
	{
	}
};
Vue.createApp({
	components: {
		'modal': ComBsModal,
		'matches': Matches,
	},
	data()
	{
		return {
			service: new Service(),
			project_id: null,
			matches: [],
			items: [],
			title_items: '',
		};
	},
	methods: 
	{
		async showInfo(pId, t, name)
		{
			const type = (t == 'reps') ? 'representantes' : 'coordinadores';
			const res = await this.service.get(`/../proyectos/${pId}/${type}`);
			//console.log(res);
			this.title_items = (t == 'reps') ? `Representantes Legales - ${name}` : 'Coordinadores - ${name}';
			this.items = res.data;
			this.$refs.modal_items.show();
		},
		async getMatches(id)
		{
			const res = await this.service.get(`/sea/matches/${id}`);
			this.matches = res.data.data;
			this.$refs.modal_matches.show();
		},
		showMatches(id)
		{
			this.project_id = id;
			this.getMatches(id);
		},
		async onAssign(match)
		{
			const res = await this.service.post(`/projects/${this.project_id}/assign`, match);
			this.$refs.modal_matches.hide();
			window.location.reload();
		}
	},
	mounted()
	{
	},
	created()
	{
		
	}
}).mount('#vue-app');
