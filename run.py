from myapi import create_app, db

if __name__ == '__main__':
	app = create_app('config.dev')
	# app.app_context().push()
	app.run(debug= app.config['DEBUG'])