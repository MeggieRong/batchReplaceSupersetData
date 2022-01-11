import os
import zipfile
import re
import shutil
import zipfile


def unzip(dir_name):
    '''
    解压from和to的压缩包
    '''
    extension = ".zip"
    os.chdir(dir_name)
    for item in os.listdir(dir_name):
        if item.endswith(extension):
            file_name = os.path.abspath(item)
            zip_ref = zipfile.ZipFile(file_name)
            zip_ref.extractall(dir_name)
            zip_ref.close()
            os.remove(file_name)


def replanDir(fromDir, toDir):
    '''
    把to的database文件夹的yaml文件，直接替换from的database的yaml文件
    '''
    fromFiles = os.listdir(fromDir)
    needTotran = toDir + '\\' + os.listdir(toDir)[0] + '\\' + 'databases'
    for file_name in fromFiles:
        targetDir = fromDir + '\\' + file_name + '\\' + 'databases'
        if os.path.isdir(targetDir):
            shutil.rmtree(targetDir, ignore_errors=True)
            shutil.copytree(needTotran, targetDir)
        else:
            shutil.copytree(needTotran, targetDir)


def ChineseizationChart(fromDir_, toDir_, parama):
    '''
    由于中文导出后是Unicode，需要转为中文，也同时修改yaml名称才能识别导入
    '''
    files = os.listdir(fromDir_)
    for file_name in files:
        path = toDir_ + '\\' + file_name + '\\' + 'new' + parama
        if not os.path.exists(path):
            newFolder = os.mkdir(path)
        newFolder = path
        subDir = fromDir_ + '\\' + file_name + '\\' + parama
        if os.path.exists(subDir):
            subFileName = os.listdir(subDir)
            for subFiles in subFileName:
                filePath = subDir + '\\' + subFiles
                for line in open(filePath):
                    if "slice_name" in line or "dashboard_title" in line:
                        needToBeUpdate = (line.split(':')[1]).split('"')[1]
                        newZh = needToBeUpdate.encode(
                            'utf-8').decode('unicode_escape')
                        fout_name = re.sub(r'[^\w\s]', '', newZh) + "_1.yaml"
                        print(fout_name)

                fin = open(filePath, "rt")
                fout = open(newFolder + '\\' + fout_name,
                            "wt", encoding="utf-8")
                for line in fin:
                    if "slice_name" in line:
                        needToBeUpdate = (line.split(':')[1]).split('"')[1]
                        newZh = needToBeUpdate.encode(
                            'utf-8').decode('unicode_escape')
                        fout.write(line.replace(needToBeUpdate, newZh))
                    else:
                        fout.write(line)
                fin.close()
                fout.close()
        shutil.rmtree(subDir, ignore_errors=True)
        os.rename(newFolder, toDir_ + '\\' + file_name + '\\' + parama)


def Update(fromDir, toDir):
    '''
    把database_uuid都改为从to导入的数据库uuid
    '''
    # 获取to的database的yaml文件的database_uuid
    needTotran = toDir + '\\' + os.listdir(toDir)[0] + '\\' + 'databases'
    sourceFile = needTotran + '\\' + os.listdir(needTotran)[0]
    for line in open(sourceFile):
        if 'uuid' in line:
            databaseUUID = line.split(':')[1]

    # 遍历From所有文件替换为新的database_uuid
    def getFile(fromDir, allFiles=[], isShow=True):
        '''
        获取所有文件绝对路径
        '''
        files = os.listdir(fromDir)
        for file in files:
            path = fromDir + '\\' + file
            if not os.path.isdir(path):
                allFiles.append(path)
            else:
                getFile(path, allFiles, False)
        if isShow:
            print('n'.join(allFiles))
        return allFiles
    fileList = getFile(fromDir)
    for filePath in fileList:
        file_data = ""
        with open(filePath, 'r', encoding="utf-8") as f:
            for line in f:
                if "database_uuid" in line:
                    needToBeUpdate = line.split(':')[1]
                    line = line.replace(needToBeUpdate, databaseUUID)
                else:
                    pass
                file_data += line
        with open(filePath, "w", encoding="utf-8") as f:
            f.write(file_data)


def zipDir(fromDir, importDir):
    '''
    将需要导入的包重新打包
    '''
    files = os.listdir(fromDir)
    for file in files:
        inputPath = fromDir + '\\' + file
        zipName = file + '.zip'
        zip = zipfile.ZipFile(importDir + '\\' + zipName,
                              "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(inputPath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(inputPath, '')
            for filename in filenames:
                zip.write(os.path.join(path, filename),
                          os.path.join(fpath, filename))
        zip.close()


def removeNUllDir(fromDir):
    files = os.listdir(fromDir)
    for i in files:
        if "dataset" in i:
            dirP = fromDir + '\\' + i
            os.removedirs(dirP + '\\' + 'charts')
            os.removedirs(dirP + '\\' + 'dashboards')
        elif "chart" in i:
            dirP = fromDir + '\\' + i
            os.removedirs(dirP + '\\' + 'dashboards')
        else:
            pass


if __name__ == '__main__':
    fromDir = 'C:\\Users\\admin\\Desktop\\replace\\From'
    toDir = 'C:\\Users\\admin\\Desktop\\replace\\to'
    importDir = 'C:\\Users\\admin\\Desktop\\replace\\import'

    unzip(fromDir)
    unzip(toDir)
    replanDir(fromDir, toDir)
    Update(fromDir, toDir)
    ChineseizationChart(fromDir, fromDir, 'charts')
    ChineseizationChart(fromDir, fromDir, 'dashboards')
    removeNUllDir(fromDir)

    # 压缩工具用不了，但windows的zip工具可以直接用
    # zipDir(fromDir, importDir)
