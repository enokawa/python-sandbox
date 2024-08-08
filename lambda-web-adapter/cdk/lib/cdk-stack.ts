import { CfnOutput, Stack, StackProps } from 'aws-cdk-lib';
import { Architecture, DockerImageCode, DockerImageFunction, FunctionUrlAuthType } from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

const path = require('path');

export class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const fn = new DockerImageFunction(this, 'LambdaWebAdapterFunction', {
      functionName: 'lambda-web-adapter-sample',
      code: DockerImageCode.fromImageAsset(path.join(__dirname, '../../src')),
      architecture: Architecture.ARM_64
    });

    const fnUrl = fn.addFunctionUrl({
      authType: FunctionUrlAuthType.NONE,
    });

    new CfnOutput(this, 'FunctionUrl', {
      value: fnUrl.url,
    });
  }
}
