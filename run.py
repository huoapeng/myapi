from myapi import create_app

if __name__ == '__main__':
    app = create_app('config.dev')
    # app = create_app('config.webapiconfig')
    # app.app_context().push()
    app.run(debug= app.config['DEBUG'])