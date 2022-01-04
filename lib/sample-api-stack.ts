import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Table, AttributeType } from 'aws-cdk-lib/aws-dynamodb'
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha'
import { LambdaRestApi } from 'aws-cdk-lib/aws-apigateway';


export class Ep05ServerlessApiStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const table = new Table(this, 'Table', {
      partitionKey: { type: AttributeType.STRING, name: 'id' },
    })

    const func = new PythonFunction(this, 'MyFunction', {
      entry: './lambda-api',
      runtime: Runtime.PYTHON_3_9,
      index: 'server.py',
      handler: 'handler',
      environment: {
        'TABLE_NAME': table.tableName
      }
    })

    new LambdaRestApi(this, 'RestAPI', {
      handler: func
    })

    table.grantReadWriteData(func)

  }
}
