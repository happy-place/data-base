package com.big.data.app.common;

/**
 * Created by atguigu on 2017/11/10
 */
public class AppStartupLog extends AppBaseLog {

    private String country;          //国家，终端不用上报，服务器自动填充该属性
    private String province;         //省份，终端不用上报，服务器自动填充该属性
    private String ipAddress;        //ip地址

    private String network;          //网络
    private String carrier;          //运营商

    private String brand;            //品牌
    private String screenSize;       //分辨率


    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getProvince() {
        return province;
    }

    public void setProvince(String province) {
        this.province = province;
    }

    public String getIpAddress() {
        return ipAddress;
    }

    public void setIpAddress(String ipAddress) {
        this.ipAddress = ipAddress;
    }

    public String getNetwork() {
        return network;
    }

    public void setNetwork(String network) {
        this.network = network;
    }

    public String getCarrier() {
        return carrier;
    }

    public void setCarrier(String carrier) {
        this.carrier = carrier;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public String getScreenSize() {
        return screenSize;
    }

    public void setScreenSize(String screenSize) {
        this.screenSize = screenSize;
    }
}
