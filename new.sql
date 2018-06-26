-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: new
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `body` varchar(256) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `author` int(11) DEFAULT NULL,
  `author_name` varchar(36) DEFAULT NULL,
  `essay` int(11) DEFAULT NULL,
  PRIMARY KEY (`cid`),
  KEY `author` (`author`),
  KEY `essay` (`essay`),
  KEY `ix_comment_time` (`time`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`author`) REFERENCES `user` (`uid`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`essay`) REFERENCES `essay` (`eid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'我是社会主义接班人','2017-06-13 09:02:46',1,1,'root',1),(2,'是你妈卖批','2017-06-13 09:02:46',1,1,'root',1),(3,'adadada','2017-06-13 09:20:16',1,1,'root',13),(4,'ssddfsfsdf','2017-06-13 09:25:32',1,1,'root',2),(5,'sdfsfsfsdf','2017-06-13 09:25:37',1,1,'root',2),(6,'dfsfsfsfxvc vxcvdcvxcv','2017-06-13 12:07:39',1,1,'root',2),(7,'sdfsdf','2017-06-15 13:33:37',1,1,'root',2),(8,'dsfsd  ','2017-06-15 14:41:49',1,1,'root',2),(9,'vvvvvvvvvvvvvvvv','2017-06-15 14:41:53',1,1,'root',2),(10,'bbbbbbbbbbbbbbbbbbbbbbbbbb','2017-06-15 14:41:58',1,1,'root',2),(11,'mmmmmmmmmmmmmmmmmm','2017-06-15 14:42:01',1,1,'root',2),(12,'adsadads','2017-06-15 14:55:29',1,1,'root',5),(13,'sdfsdf','2017-06-15 15:43:26',1,1,'root',2),(14,'sdfsdfsdf','2017-06-15 15:43:29',1,1,'root',2),(15,'sdfsfsdfsdfds','2017-06-15 15:43:32',1,1,'root',2);
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `essay`
--

DROP TABLE IF EXISTS `essay`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `essay` (
  `eid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) DEFAULT NULL,
  `essay` varchar(256) DEFAULT NULL,
  `visnum` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `visible` tinyint(1) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `author` int(11) DEFAULT NULL,
  `author_name` varchar(36) DEFAULT NULL,
  PRIMARY KEY (`eid`),
  KEY `author` (`author`),
  KEY `ix_essay_time` (`time`),
  CONSTRAINT `essay_ibfk_1` FOREIGN KEY (`author`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `essay`
--

LOCK TABLES `essay` WRITE;
/*!40000 ALTER TABLE `essay` DISABLE KEYS */;
INSERT INTO `essay` VALUES (1,'title1','hanwweibozaizhe',50,1,1,'2017-06-13 09:02:46',1,'root'),(2,'title2','woshihanweibo',216,1,0,'2017-06-13 09:02:46',1,'root'),(3,'title1','hanwweibozaizhe',10,1,1,'2017-06-13 09:08:34',1,'root'),(4,'title2','woshihanweibo',19,1,1,'2017-06-13 09:08:34',1,'root'),(5,'title1','hanwweibozaizhe',14,1,1,'2017-06-13 09:08:36',1,'root'),(6,'title2','woshihanweibo',14,1,1,'2017-06-13 09:08:36',1,'root'),(7,'title1','hanwweibozaizhe',11,1,1,'2017-06-13 09:08:38',1,'root'),(8,'title2','woshihanweibo',10,1,1,'2017-06-13 09:08:38',1,'root'),(9,'title1','hanwweibozaizhe',10,1,1,'2017-06-13 09:08:39',1,'root'),(10,'title2','woshihanweibo',10,1,1,'2017-06-13 09:08:39',1,'root'),(11,'title1','hanwweibozaizhe',10,1,1,'2017-06-13 09:08:40',1,'root'),(12,'title2','woshihanweibo',10,1,1,'2017-06-13 09:08:40',1,'root'),(13,'ssdf','sddfsfsf',3,1,1,'2017-06-13 09:20:04',1,'root'),(14,'adadsad','adadasdads',2,1,0,'2017-06-15 13:33:30',1,'root'),(15,'你好','我准备举报',3,2,1,'2017-06-15 15:38:42',1,'root'),(16,'资源共享','资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享资源共享',3,3,1,'2017-06-16 02:56:01',1,'root');
/*!40000 ALTER TABLE `essay` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) DEFAULT NULL,
  `img` blob,
  PRIMARY KEY (`mid`),
  KEY `user` (`user`),
  CONSTRAINT `image_ibfk_1` FOREIGN KEY (`user`) REFERENCES `user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image`
--

LOCK TABLES `image` WRITE;
/*!40000 ALTER TABLE `image` DISABLE KEYS */;
INSERT INTO `image` VALUES (1,1,'�PNG\r\n\Z\n\0\0\0\rIHDR\0\0z\0\0z\0\0\0\0�(\�\0\0\�IDATx�\�M�\�J�#G��o\�\�7+�ͤ�\�\r�e68�L��r?0�W��2ra�K�>@��÷�\�_\�\�P@P@P@P@�������R\�\�(��۫\�\�q\\P\�\�U\�\�v\�}�\��߼�R���\�\0\���?��G@��@��33\�\'ׇ\�\'\�v\0�=a+�/\�\'k����\�lG����X�\�\�\�\�\�\�X�+P@�x4�\�\�\�Mf3�uC��q5l�\'\�c�*����}^\r\�\0�\�U\�v?P���mG@��@�iv4\�P\��*�\�g����O\�|�h���G\�Gj\�f�O#��Ʊ\�M�\��*f�\�/�����U��LV\�\rp\�U\0�v�证�P@�9�٪�R\0l=�V��ܟnd�R�Õ\�\��վ.f\�\�\�i2\�\r(n��\��\�(���\�VJi\�	��\�kY>�V\rJ\�Q\�\�\�\�GJ4\�X>/�g5(t~\�8�T@\�S�ڔbl�?a8^Ŷ�W1�\�6@��ݿ\n�\�\"5?\�W�W\�_��\��;��W*����\Z\�\0pUwGKf��u�jf�®\�xL͆\�fM/\�\�A\��l	-�\",���;KS�PS��*�iI\���V;7�\�(U\�=	(\�@�j2\"���\��:Mf���\�}�t�\�M��H�O#��\�\0x�K�\�=wq,�m{�\�d�nxEK�W+t���ipX`giҖԏ\�G�rLWm\��0GX5�_�E�O�F@��N3�\�DS\�Mi�H4nW�ǯNoF�\�\'EX@G����\�,)\�xB�]\nWsȽ�\r7\�ZH�Y�F@\�\"m�Q%oW�pq,\�߉\rO\�\�\�^\�.\�f\�Ԭܓ�������)½��\�s\�1�8\n@L��`J�F@Gr=\r�,�\���Ӫ��y�-��	�h�<���JP��C:\r\�=isR�A�\�,z\�J_3�\�B(Y\Z\�R��fT;\���^�Ʉܻ�ݜ�OW#��{\n82�-M&�k@\�0\�F\0T\�~]�\�S�*z\Z�7˧P���]�Ե\�>�Hs�:\'\�,ǀKPqT\�\�\�(\�@Wzg�ΦV\�F&�\�\�!����hyJ�����4\n80�S����85<\�CA\n�Yd��\��G�F@G�\��zRz\��	4��S\'f\��3Yh�G>���\�|�,Л�:&>rG�\�3Y�ל��_��\n�~\�<t�\�\�%*k���z��\�{Q\r��\�\�(\�\���nδvW-La\�l�\�םG�{\�\�%D\�Wi��Z��#���y �4y�#\�\�vxY\\�P\�E?).\�!�F@��T�s\�19Q8\�~�\�/.y\�ߌ�M)\�\�\�(\�������uzl\��aϺc�d\�q\\\r[�\Z�[X|�e��\"KL5�*\�晩\���{[�4\�+P@��;�?�q\�\�k�\�\�\�_\\\�gq5*p�~�|\Z\�\�y��\nt��߲�\rT(�#\�p�0\�Nh7����\�o\�S\�ecd\�>M\�|Oƨ�׷\"G�\�\�(\�@\�{ʹy8��O=!|\0�S�\�*\��DC$vY\Z\�\�Fx�\'\��\�+�\����X\�k<�J\�\�(�$��#�\�ܣM2�j�\�6\�\�I\�\�s�,���\�sO�&c�\�<Ǧ׋i	&e�\�<i����\r��}�z���\�\�\�>*\�;��\�\�YS�1S�$����4���.u\�\�f\�8QE\�\�}f\n`G�F@G���8qm\�	�Fwb��z�XZ�R��\��\n(\��i�&��\�sۼ\�왎MD^݈r6P<}O�F@Gv�\�4\�\�Կ���\�[X�ᱮ�8��^/��P�!�}�0/\�uro�3iZf�<6�U1&�FȧP�a�\�f���\�Y�X�\��K_1�\"̩I*M�g�\�\�(\�@���\�˅��Y�K9���r����4\n8.���\�FB�L�\�,�ɯ��G\��um\��ip\\`\�8\���\�2����\�(:\�\�\0k�4nx\�a)��#�v��\�\�ܤ\�\���U,٫\�\�\�ݲ4\n8\"�-͛�\0Us5\�\�]���\�蔎��\'��>.��yp\\[E\�vC\\(�0o�:.���J�y��Ro\�ʕV���\�vP�?\�n�t]�/W%dy\rk�\�\����t�x�j�ph w\�\�},dAv�3F�\"\�t`72<{�+K#��C�F�yy�m�c�֒�;\�\n8�4�(\�S����\r<\�\�t\nn\Z3^s9�\��w�Ys\n�(9��_��\n�~�������\�+\0ڨa��G\�l������dipP [�lD�*z-\���:\�\�\�\�\�)\�\�\�(\�@\���\�f(�\�6\�hX\��\'�P5\�*pdipH`דP9/I���s]b�r�p66��\�eipd 垚,lF^K�\��]�\�I\�\�)E���.e�p\\`�\�)z#)�n�v�K+S9�ڙ\�Q�6aʧP�q�4s�\�\�Tx\�Ϗ\�\�\�\r͙\��U4�����_��\n�~R�\�r�œ~_�\�\�{\nc�ʎ����{\n( :E�jS��_tc��\\\����i\�[R�$���#\�t\n���&���]\�\��\�\���cW{xy\�\��\n(\��aE8jgzw&K\�t@\�Y҉	=\'՞l��O#��\�y7B4M�\�\�5o���}v)ª�Z�oN��P���ۍ����ݯo�\�\�\���9fE>\�\n@���r��v�V\0\�\�u\�^��\nHǳK1T\�\��2\'\��nyn��R\�i,@�\'ȡ\�1-\�A��N��\�>\�|�d�\nrfuX\n(\���n[\�\��l�5Q�W/�	bO&e\�\�4\��,�,���<\�:\�\�\�HL�\�x�\'��f�\�ͩ�\�\�R��t>\�\�\�\�{d�C\�\r?���\�\�O\�\�\�\�\r���P����3�\�4\�ܙ���x�\�C��\�u\Z*�F@,\�D2���\'+��e�ϫ\�\�l=J�v�}O\��B��\�2\��QJ�\�#���c�\�\�\�R�Wy\�17[�*�\�r�B\�͝�U\�\0(�|\�ln��y�\n( ��\\\\�\���N�w\�[\�\�n MN�ɫ��P@?\�g)\�c�\�\�^�Z�\��U}�u��V碖\\�\�|�g-�\�\Ze��w�\�\�\�\�<��\��P\�r�3[\�h���3�ipX`7�fO\�\�\'IЉ\�쿤�4����b\�<s\�{P���\\1�\�\�極H\�&\�д-�Ѱ���rk�v#(\�\��b����\�\�~�+P@P@P@P@��οk���0R\�\0\0\0\0IEND�B`�');
/*!40000 ALTER TABLE `image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tip`
--

DROP TABLE IF EXISTS `tip`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tip` (
  `tid` int(11) NOT NULL AUTO_INCREMENT,
  `eid` int(11) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `deal` tinyint(1) DEFAULT NULL,
  `deal_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`tid`),
  UNIQUE KEY `eid` (`eid`),
  UNIQUE KEY `cid` (`cid`),
  KEY `ix_tip_tid` (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tip`
--

LOCK TABLES `tip` WRITE;
/*!40000 ALTER TABLE `tip` DISABLE KEYS */;
INSERT INTO `tip` VALUES (20,2,NULL,1,1),(21,NULL,15,0,0),(22,NULL,14,0,0),(23,NULL,11,0,0),(24,14,NULL,1,1);
/*!40000 ALTER TABLE `tip` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `pwd` varchar(64) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `permission` int(11) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `ix_user_uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'root','1105066510@qq.com','rrrr',33,8),(2,'admin','1160965893@qq.com','admin',10,4),(3,'mamaoj','110965893@qq.com','admin',10,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-16 12:00:46
