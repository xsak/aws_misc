if [ "Xy$1X" = "XyX" ]
then
  echo "Need a function name"
  exit 99
else
    rm tmp.zip
    zip tmp.zip ${1}.py && \
    aws lambda update-function-code --function-name ${1} --zip-file fileb://tmp.zip --region eu-central-1
fi
