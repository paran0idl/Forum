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
INSERT INTO `comment` VALUES (1,'æˆ‘æ˜¯ç¤¾ä¼šä¸»ä¹‰æŽ¥ç­äºº','2017-06-13 09:02:46',1,1,'root',1),(2,'æ˜¯ä½ å¦ˆå–æ‰¹','2017-06-13 09:02:46',1,1,'root',1),(3,'adadada','2017-06-13 09:20:16',1,1,'root',13),(4,'ssddfsfsdf','2017-06-13 09:25:32',1,1,'root',2),(5,'sdfsfsfsdf','2017-06-13 09:25:37',1,1,'root',2),(6,'dfsfsfsfxvc vxcvdcvxcv','2017-06-13 12:07:39',1,1,'root',2),(7,'sdfsdf','2017-06-15 13:33:37',1,1,'root',2),(8,'dsfsd  ','2017-06-15 14:41:49',1,1,'root',2),(9,'vvvvvvvvvvvvvvvv','2017-06-15 14:41:53',1,1,'root',2),(10,'bbbbbbbbbbbbbbbbbbbbbbbbbb','2017-06-15 14:41:58',1,1,'root',2),(11,'mmmmmmmmmmmmmmmmmm','2017-06-15 14:42:01',1,1,'root',2),(12,'adsadads','2017-06-15 14:55:29',1,1,'root',5),(13,'sdfsdf','2017-06-15 15:43:26',1,1,'root',2),(14,'sdfsdfsdf','2017-06-15 15:43:29',1,1,'root',2),(15,'sdfsfsdfsdfds','2017-06-15 15:43:32',1,1,'root',2);
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
INSERT INTO `essay` VALUES (1,'title1','hanwweibozaizhe',50,1,1,'2017-06-13 09:02:46',1,'root'),(2,'title2','woshihanweibo',216,1,0,'2017-06-13 09:02:46',1,'root'),(3,'title1','hanwweibozaizhe',10,1,1,'2017-06-13 09:08:34',1,'root'),(4,'title2','woshihanweibo',19,1,1,'2017-06-13 09:08:34',1,'root'),(5,'title1','hanwweibozaizhe',14,1,1,'2017-06-13 09:08:36',1,'root'),(6,'title2','woshihanweibo',14,1,1,'2017-06-13 09:08:36',1,'root'),(7,'title1','hanwweibozaizhe',11,1,1,'2017-06-13 09:08:38',1,'root'),(8,'title2','woshihanweibo',10,1,1,'2017-06-13 09:08:38',1,'root'),(9,'title1','hanwweibozaizhe',10,1,1,'2017-06-13 09:08:39',1,'root'),(10,'title2','woshihanweibo',10,1,1,'2017-06-13 09:08:39',1,'root'),(11,'title1','hanwweibozaizhe',10,1,1,'2017-06-13 09:08:40',1,'root'),(12,'title2','woshihanweibo',10,1,1,'2017-06-13 09:08:40',1,'root'),(13,'ssdf','sddfsfsf',3,1,1,'2017-06-13 09:20:04',1,'root'),(14,'adadsad','adadasdads',2,1,0,'2017-06-15 13:33:30',1,'root'),(15,'ä½ å¥½','æˆ‘å‡†å¤‡ä¸¾æŠ¥',3,2,1,'2017-06-15 15:38:42',1,'root'),(16,'èµ„æºå…±äº«','èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«èµ„æºå…±äº«',3,3,1,'2017-06-16 02:56:01',1,'root');
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
INSERT INTO `image` VALUES (1,1,'‰PNG\r\n\Z\n\0\0\0\rIHDR\0\0z\0\0z\0\0\0\0ð(\Õ\0\0\ØIDATxœ\íMŽ\ãJ„#G¼”o\à£\È7+ôÍ¤£\Ô\r¤e68‹L’‘r?0˜Wý¦2ra”K²>@‚þÃ·ž\í_\ß\ËP@P@P@P@ÿŸ€¥°•R\Ê\ã(¥”Û«\ä\åq\\P\Ê\íU\ï\Äv\ê}\ã‚ò€ß¼•R°•°\Ý\0\àð‡?øG@üó@˜™33\Û\'×‡\ç\'\Ìv\0‹=a+ü/\Û\'kö¬÷˜\ÌlGý…­óXö\É\Ú\Ï\ê\Í\ÎXþ+P@ÿx4§\Ã\Ö\ÙMf3ûuCµÀq5l÷\'\Êcþ*¥”«™}^\r\Ë\0˜\êU\à¸v?P½¥ømG@üó@÷iv4\ËP\í†û*þ\ág©žŒ‘O\Ó|Ÿhž‘»G\ÕGj\æf’O# €Æ±\ÕM‹\Ùþ*f»\ë/‹™›ŒýUª‹LV\Ê\rp\ÈU\0Àv÷è¯ûP@ÿ9ÀÙª®R\0l=®Vó¥ÜŸndŽR€Ã•\Þ\íþÕ¾.f\æ\ê\ïµi2\Û\r(n¥š\Ô¿\í( €ÿ\àVJi\Î	€ò±\ÕkY>¯V\rJ\ÆQ\Ë\ç\Õ\ÊGJ4\ÇX>/õg5(t~\Î8¯T@\ÌS•Ú”bl»?a8^Å¶ûW1€\Ë6@ýºÝ¿\n¶\Û\"5?\ëW«W\ï_õÀ\Ü÷;üüW* €¾Ÿ\Z\í\0pUwGKf¯ðœu½jf”Â®\íxLÍ†\ÏfM/\Þ\áA\×ül	-“\", €£;KS³PS˜³*‡iI\ãø…V;7·\Æ(U\Ê=	(\à°@j2\"½ƒ\êõ:Mf¯«³\ä}öt§\ÈM‹ûHO# €\Ý\0xÁKþ\Ï=wq,ªm{‚\ëd¢nxEK“W+t•€òipX`giÒ–Ô\ÖGrLWm\Ãñ0GX5·_¹EýO–F@‡†N3™\ÕDS\ÜMi±H4nW½Ç¯NoF«\Ý\'EX@Gº“±¢\É,)\ßxBŸ]\nWsÈ½‘\r7\ïZH™Y–F@\Ç\"m‰Q%oW¦pq,\Ôß‰\rO\ë\à\Î^\î.\ã´f\ãÔ¬Ü“€Ž¤©ù•­)Â½¾›\í“s\È1ð8\n@Lœˆ`J–F@Gr=\r¼,\×‘žÓªôžy¥-¡˜	ðhŒ<£ŸÿJPÀ÷C:\r\Å=isR¢Aó\Ä,z\ÔJ_3\ÕB(Y\Z\áRªºfT;\Ãõ¢^¡É„Ü»¢Ýœ’OW#¬™{\n82-M&¤k@\å0\ÕF\0T\Ó~]•\ÞS¢*z\Z7Ë§PÀ‘]ôÔµ\Ô>‚Hs¦:\'\Ï,Ç€KPqT\Û\È\Ò(\à¨@Wzg£Î¦V\ÃF&’\Þ\í!½„²hyJù˜£§²4\n80ðœSòÿ¥µ85<\ÉCA\n¿Yd™\Ô•G–F@Gò\ÄòzRz\Ùû	4õ–S\'f\Öú3Yh“G>€ü\Í|š,Ð›¸:&>rGý\ì3Y”×œûó_©€\nø~\Ò<tŽ\È\Ä%*kºÿz¾ó\ê{Q\r—þ\É\Ò(\à\ÈÀºnÎ´vW-La\Ðl–\ì×Gð•{\Ë\ç%D\ãWiý¼Zü¾# €þy û4yš#\â\ívxY\\óP\ÞE?).\Û!F@¾µT®s\Ê19Q8\Ê~£\Â/.y\ÄßŒ°M)\Û\È\Ò(\àÀÀ¶©®uzl\å‚òaÏºcÀd\åq\\\r[¹\Z«[X|‡e¹ú\"KL5¶*\åæ™©\íþ¬{[š4\Ê+P@ù¸;óž?Šq\ä\Ík‰\ê˜\êµ\Ä_\\\ágq5*pÀ~“|\Z\Ø\èy÷À\ntý³ß²ö\rT(¼#\Êp¼0\ÆNh7‚€Œ‰\åo\ã‚S\ßecd\Æ>M\Õ|OÆ¨Ÿ×·\"G†\Ê\Ò(\à @\î{Ê¹y8µõO=!|\0­SŠ\Ã*\Ú÷DC$vY\Z\Ø\ïFx†\'\ãƒòš\Ö+œ\Îþ‹…X\Ók<ˆJ\ãª\â(÷$ €#û\ÝÜ£M2™jˆ\Ê6\Ü\ÏI\È\ã­s·,€Ž\ìsO–&c©\Ä<Ç¦×‹i	&e¦\Ü<iŽ°€Ž\r†}•z…›š\Ú\É\â>*\Ð;¥¢\Ò\ãYS§1Sô$ €ûù4ýüˆ.u\ä‰\ëf\Ì8QE\Í\Û}f\n`G–F@Göûž8qm\Í	¹Fwbº¯z²XZ™Ríº¤ù\Ï¥\n(\àûi–&ƒ¤\ÝsÛ¼\ä ì™ŽMD^Ýˆr6P<}O–F@Gv›\å4\á\ÄÔ¿€“þ\Â[Xªá±®‚8”^/–¥PÀ!}0/\Åuroª3iZf£<6…U1&‚FÈ§PÀa\Ýf¹Œ€\àY¨Xð\äþK_1“\"Ì©I*M‹gµ\ä\Ó(\à¸@ŠžŒ\×Ë…Â’­’YñK9Œÿr¡‡õù4\n8.°¯ý\íFBL‰\ë, É¯“ñG\Öõum\Üòip\\`\×8\à“\Í2œª€û\Ð(:\Ú\É\0kù4nx\Ôa) €#Áv£¯\×\ëÜ¤\â¤\ëòûU,Ù«\à\Í\ÕÝ²4\n8\"-Í›µ\0Us5\Ò\í]¥ú¿\Öè”Ž¢\'°>.Àòyp\\[E\ÞvC\\(¥0o’:.À²¿J½y±¯Ro\ÙÊ•V¶œ€\ßvPÀ?\än„t]¢/W%dy\rk¾\Ý\ÕúÀ…tŸx²j„ph w\ä\É},dAv 3F\"\Üt`72<{‚+K# €C£F¸yy÷möc»Ö’£;\à­\n8ú4—(\éS‡¥€Ž\r<\×\Ót\nn\Z3^s9û\×¨wšYs\nµ(9þó_©€\nø~š˜»‘¹¥ñ\Ý+\0Ú¨ažªG\ÉlŽ·ºô§¢dipP [šlD *z-\Ïûž:\Ó\Ò\Í\É\â)\ì\É\Ò(\à¨@\Þò‹\ê•f(ž\à6\ËhX\è‡»\'“P5\ï*pdipH`×“P9/I ø¨s]b£r„p66‘\Ùeipd åžš,lF^K–\Íø]¸\ÍI\Ù\Ü)Eý—ý.e¹p\\`¿\ï)z#)ùn—v‘K+S9ŽÚ™\ÌQ6aÊ§PÀq4s\Ó\ÕTx\×Ï\Ø\Þ\åŽ\rÍ™\à”U4ˆ§¨óó_©€\nø~R§\Ér§Å“~_”\×\ì™{\nc”ÊŽ±¼£™{\n( :E˜jS¦Š_tcôö\\\Ý¶¤÷i\Â[Rô$ €ƒ#\Ït\n¡²Š&ýœ–]\Ê\Äò­\ä\ÎÀ•cW{xy\Ë\Ï¥\n(\àûaE8jgzw&K\Ôt@\ëYÒ‰	=\'Õžl¸”O# €\Ãy7B4M²\Ò\å5o£Ÿ}v)Âª¾Z¸oN¥PÀ‘Û‡•—Ý¯o·\É\Ê\ã¸ø÷9fE>\æ\n@“”r°•vÁV\0\å\Ãu\å^©€\nHÇ³K1T\ì\çð2\'\ä‰nynÿ”R\Ãi,@¹\'È¡\Ë1-\äA¤¢N»»\â>\×|³d˜\nrfuX\n(\àðÀn[\î\îÿl•5QŒW/¤	bO&e\î\É4\î§,”,€Ž<\çž:\×\Å\ÍHL¦\Úx§\'ªòfÀ\ÍÍ©£\ê\ç¿Rðýt>\Í\ä\í\Ù{d¯C\Ë\r?‡†\Ç\ìO\ä\à\à¸\Ú\r ¥PÀ‘¼3»\é4\èÜ™Œ…¢x\ÇC˜\Üu\Z*F@,\íD2»¦«\'+ÿŠe³Ï«\Ç\Õl=JÁvó}O\í¯B²ð¯\Ò2\ßÀQJü\Æ# €þc€\ì\Ä\äR–Wy\Û17[ñ*¥\Ür›B\îÍ¬U\Ö\0(|\Ôln´†y¥\n( Ž™\\\\ù\ÝÀžN¾w\Ë[\Ú\Õn MN¯É«ŠžP@?\Ëg)\åc÷\ê\Þ^¥Z\íþU}ûu›¬Vç¢–\\ÿ\Ô|Ÿg-®\é©\Zeýøwð\Ï\ï\Ó\Ð<¯‰\áòšP\Ïr·3[\Ëh¯þ¹3òipX`7ŸfO\é\Å\'IÐ‰\Ëì¿¤ù4‘¼Š‚b\Ä<s\í{PÀÁ\\1»\ãŒ\ææ¥µH\í&\ÆÐ´-“Ñ°‰ô‘rk”v#(\à\ØÀbÿùžÿ\å\Ù~þ+P@P@P@P@ü¯Î¿k«¿–0R\â»\0\0\0\0IEND®B`‚');
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
