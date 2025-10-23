class Service
{
	constructor()
	{
		this.apibase = AppConfig.baseurl + '/api';
	}
	async request(endpoint, method, data, $headers)
	{
		let headers = {
			'Content-Type': 'application/json',
			//'Access-Control-Allow-Origin': '*',
			//'Origin': 'https://localhost'
		};
		let token = localStorage.getItem('jwt');
		if( token )
		{
			headers['Authorization'] = 'Bearer ' + token;
		}
		if( typeof $headers == 'object' )
		{
			for(let key in $headers)
			{
				headers[key] = $headers[key];
			}
		}
		let ops = {
			method: method,
			body: ( method == 'POST' || method == 'PUT' && data) ? ( typeof data == 'object' ? JSON.stringify(data) : data ) : null,
			mode: 'cors',
			cache: 'no-cache',
			headers: headers,
			//credentials: 'include', //'omit'
		};
		const url = this.apibase + endpoint;
		const xhr = await fetch(url, ops);
		if( !xhr.ok )
			throw {error: '', code: xhr.status, data: await xhr.json()};
		const rdata = await xhr.json();
		const res = {
			headers: xhr.headers,
			xhr: xhr,
			data: rdata,
		};
		return res;
	}
	async get(endpoint, headers)
	{
		return await this.request(endpoint, 'GET', null, headers);
	}
	async post(endpoint, data, headers)
	{
		return await this.request(endpoint, 'POST', data, headers);
	}
	async put(endpoint, data, headers)
	{
		return await this.request(endpoint, 'PUT', data, headers);
	}
}
export default Service;
