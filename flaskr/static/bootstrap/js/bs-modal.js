const ComBsModal = {
		template: `<div class="modal" v-bind:class="{'fade': fade }" ref="modal">
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="header-title">{{ title }}</h5>
						<slot name="header"></slot>
					</div>
					<div class="modal-body">
						<slot></slot>
					</div>
					<div class="modal-footer">
						<slot name="footer"></slot>
						<button type="button" class="btn btn-danger" data-dismiss="modal" data-bs-dismiss="modal" data-coreui-dismiss="modal"
							v-on:click="cancel()">
							{{ cancelText }}
						</button>
						<button type="button" class="btn btn-primary" v-if="submitText !== null" v-on:click="submit()">{{ submitText }}</button>
					</div>
				</div>
			</div>
		</div>`,
		props: {
			fade: {type: Boolean, required: false, default: false},
			title: {type: String, required: true, default: ''},
			cancelText: {type: String, required: false, default: 'Cancelar/Cerrar'},
			submitText: {type: String, required: false, default: 'Guardar'},
		},
		data()
		{
			return {
				modal: null,
			};
		},
		methods: 
		{
			hide()
			{
				if( this.modal.hide )
				{
					this.modal.hide();
				}
				else if( window.jQuery )
				{
					jQuery(this.modal).modal('hide');
				}
				this.$emit('hide', {com: this});
			},
			show()
			{
				if( this.modal.show )
				{
					this.modal.show();
				}
				else if( window.jQuery )
				{
					jQuery(this.modal).modal('show');
				}
				this.$emit('show', {com: this});
			},
			cancel()
			{
				this.hide();
				this.$emit('cancel', {com: this});
			},
			submit()
			{
				this.$emit('submit', {com: this});
			}
		},
		mounted()
		{
			const frame = (window.bootstrap || window.coreui);
			this.modal = frame ? frame.Modal.getOrCreateInstance(this.$refs.modal) : this.$refs.modal; 
		},
		created()
		{
			
		}
	};
export default ComBsModal;
